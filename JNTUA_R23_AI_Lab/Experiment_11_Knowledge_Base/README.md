# Experiment 11: Knowledge-Based System (Family Relations)

**Artificial Intelligence Lab | Subject Code 23A31301P | JNTUA R23 | B.Tech AI & DS**

## Aim

To build a small knowledge base of facts and inference rules, allow queries, and explain the conclusions reached.

## Theory

A **knowledge-based system** separates **knowledge** (facts and rules) from the **inference engine** that reasons with it.

* **Facts** state basic truths: `parent(tom, bob).`
* **Rules** (Horn clauses) derive new facts: `grandparent(X, Z) :- parent(X, Y), parent(Y, Z).` means *X is a grandparent of Z IF X is a parent of some Y AND Y is a parent of Z*.
* **Backward chaining** starts from the query (goal) and works backwards: find a fact that matches, or a rule whose head unifies with the goal and then prove each condition in the rule body.
* **Explanation:** every answer is printed with its proof tree showing which facts and rules were used.
* **Closed-world assumption:** if a statement cannot be proven, the system answers *No*.
* Built-in `neq(A, B)` succeeds when A and B are different constants (used to define `sibling`).

## Algorithm / Procedure

1. Parse the knowledge base text into facts and rules.
2. Parse the query (e.g. `grandparent(tom, W)`).
3. `prove(goal)`: for each KB clause, rename its variables to fresh names and unify its head with the goal. If it unifies, prove all body goals in order, passing the bindings along (recursion).
4. Each success yields a substitution and a proof tree. Remove duplicate answers.
5. Print the bindings of the query variables and the proof tree. If there is no proof, print *No*.
6. A depth limit prevents endless recursion.

## Source Code

The complete program is in [`main.py`](main.py) and is reproduced here.

```python
"""
Experiment 11: Knowledge-Based System (family relationships)
Subject: Artificial Intelligence Lab (23A31301P) - JNTUA R23

A knowledge base (KB) holds FACTS and RULES written as Horn clauses:
    parent(tom, bob).                                  <- fact
    grandparent(X, Z) :- parent(X, Y), parent(Y, Z).   <- rule: head IF body
Variables start with an uppercase letter; constants with lowercase.

Inference engine: BACKWARD CHAINING (goal-driven, like Prolog).
To prove a goal it looks for a fact that matches, or a rule whose head
unifies with the goal and then tries to prove every goal in the rule body.
Each answer is shown together with the proof (explanation) that supports it.
Closed-world assumption: anything that cannot be proven is reported as false.
Built-in predicate: neq(A, B) succeeds when A and B are different constants.
"""

import itertools
import re
from dataclasses import dataclass

KB_TEXT = """
parent(tom, bob).     parent(pam, bob).
parent(tom, liz).     parent(pam, liz).
parent(bob, ann).     parent(bob, pat).
parent(liz, jim).     parent(pat, joe).

male(tom).  male(bob).  male(jim).  male(pat).  male(joe).
female(pam). female(liz). female(ann).

father(X, Y)      :- parent(X, Y), male(X).
mother(X, Y)      :- parent(X, Y), female(X).
grandparent(X, Z) :- parent(X, Y), parent(Y, Z).
sibling(X, Y)     :- parent(P, X), parent(P, Y), neq(X, Y).
uncle(U, N)       :- sibling(U, P), parent(P, N), male(U).
ancestor(X, Y)    :- parent(X, Y).
ancestor(X, Y)    :- parent(X, Z), ancestor(Z, Y).
"""

SAMPLE_QUERIES = [
    "father(tom, bob)",
    "grandparent(tom, W)",
    "sibling(ann, S)",
    "ancestor(pam, joe)",
    "mother(tom, bob)",
]
MAX_DEPTH = 40          # protects against endless recursion
MAX_ANSWERS = 20


@dataclass(frozen=True)
class Var:
    name: str
    uid: int = 0          # uid > 0 marks a renamed copy of a rule variable

    def __str__(self):
        return self.name if self.uid == 0 else f"{self.name}_{self.uid}"


@dataclass(frozen=True)
class Compound:
    functor: str
    args: tuple

    def __str__(self):
        if not self.args:
            return self.functor
        return f"{self.functor}({', '.join(str(a) for a in self.args)})"


@dataclass
class Rule:
    head: Compound
    body: list
    text: str


def ask(prompt, default):
    try:
        text = input(prompt).strip()
    except EOFError:
        return default
    return text if text else default


# ------------------------------ parsing -------------------------------
def tokenize(text):
    return re.findall(r":-|[A-Za-z0-9_]+|[(),.?]|\S", text)


class Parser:
    def __init__(self, text):
        self.tokens = tokenize(text)
        self.pos = 0

    def peek(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def take(self, expected=None):
        token = self.peek()
        if token is None or (expected is not None and token != expected):
            raise ValueError(f"expected '{expected}' but found '{token}'")
        self.pos += 1
        return token

    def term(self):
        name = self.take()
        if not re.fullmatch(r"[A-Za-z0-9_]+", name):
            raise ValueError(f"unexpected symbol '{name}'")
        if self.peek() == "(":
            self.take("(")
            args = [self.term()]
            while self.peek() == ",":
                self.take(",")
                args.append(self.term())
            self.take(")")
            return Compound(name, tuple(args))
        if name[0].isupper() or name[0] == "_":
            return Var(name)
        return Compound(name, ())                  # constant = compound with no args

    def clause(self):
        head = self.term()
        body = []
        if self.peek() == ":-":
            self.take(":-")
            body.append(self.term())
            while self.peek() == ",":
                self.take(",")
                body.append(self.term())
        self.take(".")
        return head, body


def load_kb(text):
    """Parse KB text. Returns a list of Rule objects (facts have an empty body)."""
    parser, rules = Parser(text), []
    while parser.peek() is not None:
        start = parser.pos
        head, body = parser.clause()
        source = " ".join(parser.tokens[start:parser.pos])
        source = re.sub(r"\s+([,.)])", r"\1", source).replace("( ", "(")
        source = re.sub(r"\s*\(\s*", "(", source)
        rules.append(Rule(head, body, source))
    return rules


def parse_query(text):
    text = text.strip().rstrip(".?").strip()
    parser = Parser(text)
    goal = parser.term()
    if parser.peek() is not None:
        raise ValueError(f"unexpected symbol '{parser.peek()}'")
    return goal


# --------------------------- unification ------------------------------
def walk(term, subst):
    while isinstance(term, Var) and term in subst:
        term = subst[term]
    return term


def resolve(term, subst):
    term = walk(term, subst)
    if isinstance(term, Compound):
        return Compound(term.functor, tuple(resolve(a, subst) for a in term.args))
    return term


def occurs(var, term, subst):
    term = walk(term, subst)
    if term == var:
        return True
    return isinstance(term, Compound) and any(occurs(var, a, subst) for a in term.args)


def unify(x, y, subst):
    x, y = walk(x, subst), walk(y, subst)
    if x == y:
        return subst
    if isinstance(x, Var) or isinstance(y, Var):
        var, other = (x, y) if isinstance(x, Var) else (y, x)
        if occurs(var, other, subst):
            return None
        new_subst = dict(subst)
        new_subst[var] = other
        return new_subst
    if x.functor != y.functor or len(x.args) != len(y.args):
        return None
    for a, b in zip(x.args, y.args):
        subst = unify(a, b, subst)
        if subst is None:
            return None
    return subst


def has_variable(term):
    if isinstance(term, Var):
        return True
    return any(has_variable(a) for a in term.args)


# --------------------------- inference engine -------------------------
class Engine:
    def __init__(self, rules):
        self.rules = rules
        self.counter = itertools.count(1)

    def rename(self, term, uid):
        """Give a rule's variables fresh names so different uses do not clash."""
        if isinstance(term, Var):
            return Var(term.name, uid)
        return Compound(term.functor, tuple(self.rename(a, uid) for a in term.args))

    def prove(self, goal, subst, depth):
        """Generate (substitution, proof) pairs for one goal."""
        if depth > MAX_DEPTH:
            return
        if goal.functor == "neq" and len(goal.args) == 2:          # built-in
            a, b = resolve(goal.args[0], subst), resolve(goal.args[1], subst)
            if not has_variable(a) and not has_variable(b) and a != b:
                yield subst, (goal, "built-in: the two arguments are different", [])
            return
        for rule in self.rules:
            uid = next(self.counter)
            head = self.rename(rule.head, uid)
            new_subst = unify(goal, head, subst)
            if new_subst is None:
                continue
            body = [self.rename(g, uid) for g in rule.body]
            label = "fact in KB" if not rule.body else f"rule  {rule.text}"
            for final_subst, sub_proofs in self.prove_all(body, new_subst, depth + 1):
                yield final_subst, (goal, label, sub_proofs)

    def prove_all(self, goals, subst, depth):
        """Prove a list of goals one after another (they share variable bindings)."""
        if not goals:
            yield subst, []
            return
        for s1, proof in self.prove(goals[0], subst, depth):
            for s2, rest in self.prove_all(goals[1:], s1, depth):
                yield s2, [proof] + rest

    def ask(self, query):
        """Return a list of (answer bindings, proof), without duplicate answers."""
        query_vars = []

        def collect(term):
            if isinstance(term, Var):
                if term not in query_vars:
                    query_vars.append(term)
            else:
                for a in term.args:
                    collect(a)
        collect(query)

        answers, seen = [], set()
        for subst, proof in self.prove(query, {}, 0):
            bindings = tuple((v.name, str(resolve(v, subst))) for v in query_vars)
            if bindings not in seen:
                seen.add(bindings)
                answers.append((bindings, resolve_proof(proof, subst)))
            if len(answers) >= MAX_ANSWERS:
                break
        return answers


def resolve_proof(proof, subst):
    goal, label, children = proof
    return resolve(goal, subst), label, [resolve_proof(c, subst) for c in children]


def print_proof(proof, indent=0):
    goal, label, children = proof
    print("      " + "  " * indent + f"{goal}   [{label}]")
    for child in children:
        print_proof(child, indent + 1)


def run_query(engine, text):
    print(f"\n?- {text}")
    try:
        query = parse_query(text)
    except ValueError as error:
        print(f"   Could not understand the query: {error}")
        return
    answers = engine.ask(query)
    if not answers:
        print("   No. This cannot be proven from the knowledge base (closed-world assumption).")
        return
    if answers[0][0] == ():
        print("   Yes. The statement is true because:")
        print_proof(answers[0][1])
        return
    print(f"   Yes, {len(answers)} answer(s):")
    for number, (bindings, proof) in enumerate(answers, start=1):
        print(f"   {number}. " + ", ".join(f"{n} = {v}" for n, v in bindings))
        print("      Why:")
        print_proof(proof)


def main():
    print("=" * 60)
    print("EXPERIMENT 11: KNOWLEDGE-BASED SYSTEM")
    print("=" * 60)
    rules = load_kb(KB_TEXT)
    engine = Engine(rules)
    facts = [r for r in rules if not r.body]
    print(f"Knowledge base loaded: {len(facts)} facts and {len(rules) - len(facts)} rules.")
    print("\nRules:")
    for rule in rules:
        if rule.body:
            print("   " + rule.text)

    print("\n--- Sample queries ---")
    for text in SAMPLE_QUERIES:
        run_query(engine, text)

    print("\n--- Ask your own questions ---")
    print("Examples: uncle(U, jim)   ancestor(X, joe)   father(F, ann)")
    print("Commands: 'facts' lists the facts; press Enter or type 'quit' to exit.")
    while True:
        text = ask("\n?- ", "quit")
        if text.lower() in ("quit", "exit", "q"):
            break
        if text.lower() == "facts":
            for fact in facts:
                print("   " + fact.text)
            continue
        run_query(engine, text)
    print("\nGoodbye.")


if __name__ == "__main__":
    main()
```

## Sample Input

Five built-in sample queries run first. Then type your own, e.g. `uncle(U, jim)`, `ancestor(X, joe)`, `facts`, or `quit`.

## Expected Output

The outputs below were produced by actually running `main.py` (Python 3.12) with the inputs shown; text after each prompt is the input that was typed.

**Sample queries and two user queries**

```text
============================================================
EXPERIMENT 11: KNOWLEDGE-BASED SYSTEM
============================================================
Knowledge base loaded: 16 facts and 7 rules.

Rules:
   father(X, Y) :- parent(X, Y), male(X).
   mother(X, Y) :- parent(X, Y), female(X).
   grandparent(X, Z) :- parent(X, Y), parent(Y, Z).
   sibling(X, Y) :- parent(P, X), parent(P, Y), neq(X, Y).
   uncle(U, N) :- sibling(U, P), parent(P, N), male(U).
   ancestor(X, Y) :- parent(X, Y).
   ancestor(X, Y) :- parent(X, Z), ancestor(Z, Y).

--- Sample queries ---

?- father(tom, bob)
   Yes. The statement is true because:
      father(tom, bob)   [rule  father(X, Y) :- parent(X, Y), male(X).]
        parent(tom, bob)   [fact in KB]
        male(tom)   [fact in KB]

?- grandparent(tom, W)
   Yes, 3 answer(s):
   1. W = ann
      Why:
      grandparent(tom, ann)   [rule  grandparent(X, Z) :- parent(X, Y), parent(Y, Z).]
        parent(tom, bob)   [fact in KB]
        parent(bob, ann)   [fact in KB]
   2. W = pat
      Why:
      grandparent(tom, pat)   [rule  grandparent(X, Z) :- parent(X, Y), parent(Y, Z).]
        parent(tom, bob)   [fact in KB]
        parent(bob, pat)   [fact in KB]
   3. W = jim
      Why:
      grandparent(tom, jim)   [rule  grandparent(X, Z) :- parent(X, Y), parent(Y, Z).]
        parent(tom, liz)   [fact in KB]
        parent(liz, jim)   [fact in KB]

?- sibling(ann, S)
   Yes, 1 answer(s):
   1. S = pat
      Why:
      sibling(ann, pat)   [rule  sibling(X, Y) :- parent(P, X), parent(P, Y), neq(X, Y).]
        parent(bob, ann)   [fact in KB]
        parent(bob, pat)   [fact in KB]
        neq(ann, pat)   [built-in: the two arguments are different]

?- ancestor(pam, joe)
   Yes. The statement is true because:
      ancestor(pam, joe)   [rule  ancestor(X, Y) :- parent(X, Z), ancestor(Z, Y).]
        parent(pam, bob)   [fact in KB]
        ancestor(bob, joe)   [rule  ancestor(X, Y) :- parent(X, Z), ancestor(Z, Y).]
          parent(bob, pat)   [fact in KB]
          ancestor(pat, joe)   [rule  ancestor(X, Y) :- parent(X, Y).]
            parent(pat, joe)   [fact in KB]

?- mother(tom, bob)
   No. This cannot be proven from the knowledge base (closed-world assumption).

--- Ask your own questions ---
Examples: uncle(U, jim)   ancestor(X, joe)   father(F, ann)
Commands: 'facts' lists the facts; press Enter or type 'quit' to exit.

?- uncle(U, jim)

?- uncle(U, jim)
   Yes, 1 answer(s):
   1. U = bob
      Why:
      uncle(bob, jim)   [rule  uncle(U, N) :- sibling(U, P), parent(P, N), male(U).]
        sibling(bob, liz)   [rule  sibling(X, Y) :- parent(P, X), parent(P, Y), neq(X, Y).]
          parent(tom, bob)   [fact in KB]
          parent(tom, liz)   [fact in KB]
          neq(bob, liz)   [built-in: the two arguments are different]
        parent(liz, jim)   [fact in KB]
        male(bob)   [fact in KB]

?- father(F

?- father(F
   Could not understand the query: expected ')' but found 'None'

?- quit

Goodbye.
```

## Result

The system answers queries about fathers, mothers, grandparents, siblings, uncles and ancestors (including recursive ancestor rules) and shows a proof for each conclusion. Unprovable queries return *No*, and malformed queries produce a clear error message.

## How to Run

```bat
cd Experiment_11_Knowledge_Base
python main.py
```

From the project root you can also run `run_experiment.bat 11`.
