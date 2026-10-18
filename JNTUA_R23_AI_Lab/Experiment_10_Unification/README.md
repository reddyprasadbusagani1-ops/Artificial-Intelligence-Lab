# Experiment 10: Unification Algorithm (First-Order Logic)

**Artificial Intelligence Lab | Subject Code 23A31301P | JNTUA R23 | B.Tech AI & DS**

## Aim

To implement the unification algorithm for first-order logic with substitutions, compound terms and an occurs check, and to demonstrate successful and failed unification.

## Theory

**Unification** finds a **substitution** (a mapping from variables to terms) that makes two logical expressions identical. It is the core operation of resolution theorem proving and of Prolog.

Notation used: variables start with an **uppercase** letter (`X`, `Y`); constants and functor names start with a **lowercase** letter (`a`, `john`, `f`); compound terms look like `f(X, g(a))`.

Failure cases: two different constants; different functors; different number of arguments (arity); or the **occurs check** - a variable cannot be bound to a term that contains the same variable (e.g. `X` and `f(X)`), because that would create an infinite term. The result is the **most general unifier** (MGU).

## Algorithm / Procedure

`unify(x, y, subst)`:
1. Apply existing bindings to x and y (`walk`).
2. If x and y are identical, return the substitution unchanged.
3. If x is a variable: if x occurs inside y (**occurs check**) fail; otherwise bind x -> y. Do the same if y is a variable.
4. If both are compound terms: if the functor or arity differs, fail; otherwise unify the arguments one by one, carrying the substitution forward.
5. Otherwise (e.g. two different constants) fail.

The program then applies the substitution to both terms and checks that the results are identical.

## Source Code

The complete program is in [`main.py`](main.py) and is reproduced here.

```python
"""
Experiment 10: Unification Algorithm (First-Order Logic)
Subject: Artificial Intelligence Lab (23A31301P) - JNTUA R23

Unification finds a SUBSTITUTION that makes two logical terms identical.

Term notation used by this program (Prolog style):
  Variable : starts with an UPPERCASE letter or underscore   X, Y, Person
  Constant : starts with a lowercase letter or digit         a, john, 5
  Compound : functor(arg1, arg2, ...)                        f(X, g(a)), loves(john, Y)

Rules of the algorithm:
  1. identical terms                    -> success, nothing to substitute
  2. variable vs term                   -> bind the variable (after an OCCURS CHECK)
  3. compound vs compound               -> same functor and arity, then unify arguments
  4. anything else (clash)              -> failure
OCCURS CHECK: X can not be unified with f(X) because that would be an infinite term.
"""

import re
from dataclasses import dataclass


@dataclass(frozen=True)
class Var:
    name: str

    def __str__(self):
        return self.name


@dataclass(frozen=True)
class Const:
    name: str

    def __str__(self):
        return self.name


@dataclass(frozen=True)
class Compound:
    functor: str
    args: tuple

    def __str__(self):
        return f"{self.functor}({', '.join(str(a) for a in self.args)})"


def ask(prompt, default):
    try:
        text = input(prompt).strip()
    except EOFError:
        return default
    return text if text else default


# ---------------------------- parsing ---------------------------------
def tokenize(text):
    tokens = re.findall(r"[A-Za-z0-9_]+|[(),]|\S", text)
    return tokens


def parse_term(text):
    """Convert text such as 'f(X, g(a))' into a term object. Raises ValueError."""
    tokens = tokenize(text)
    position = 0

    def parse():
        nonlocal position
        if position >= len(tokens):
            raise ValueError("unexpected end of input")
        token = tokens[position]
        if not re.fullmatch(r"[A-Za-z0-9_]+", token):
            raise ValueError(f"unexpected symbol '{token}'")
        position += 1
        if position < len(tokens) and tokens[position] == "(":
            position += 1
            args = [parse()]
            while position < len(tokens) and tokens[position] == ",":
                position += 1
                args.append(parse())
            if position >= len(tokens) or tokens[position] != ")":
                raise ValueError("missing closing parenthesis")
            position += 1
            if token[0].isupper() or token[0] == "_":
                raise ValueError(f"functor '{token}' must start with a lowercase letter")
            return Compound(token, tuple(args))
        if token[0].isupper() or token[0] == "_":
            return Var(token)
        return Const(token)

    term = parse()
    if position != len(tokens):
        raise ValueError(f"unexpected symbol '{tokens[position]}'")
    return term


# --------------------------- unification ------------------------------
def walk(term, subst):
    """Follow variable bindings until an unbound variable or non-variable is found."""
    while isinstance(term, Var) and term in subst:
        term = subst[term]
    return term


def occurs_in(var, term, subst):
    """OCCURS CHECK: does var appear inside term (after applying bindings)?"""
    term = walk(term, subst)
    if term == var:
        return True
    if isinstance(term, Compound):
        return any(occurs_in(var, arg, subst) for arg in term.args)
    return False


def unify(x, y, subst):
    """
    Unify x and y. Returns an extended substitution (dict) or None on failure.
    The input substitution is never modified.
    """
    x, y = walk(x, subst), walk(y, subst)
    if x == y:
        return subst
    if isinstance(x, Var):
        return bind(x, y, subst)
    if isinstance(y, Var):
        return bind(y, x, subst)
    if isinstance(x, Compound) and isinstance(y, Compound):
        if x.functor != y.functor or len(x.args) != len(y.args):
            return None                                   # functor/arity clash
        for a, b in zip(x.args, y.args):
            subst = unify(a, b, subst)
            if subst is None:
                return None
        return subst
    return None                                           # constant clash etc.


def bind(var, term, subst):
    if occurs_in(var, term, subst):
        return None                                       # occurs check failed
    new_subst = dict(subst)
    new_subst[var] = term
    return new_subst


def resolve(term, subst):
    """Apply the substitution completely (replace variables inside compounds too)."""
    term = walk(term, subst)
    if isinstance(term, Compound):
        return Compound(term.functor, tuple(resolve(a, subst) for a in term.args))
    return term


def explain_failure(x, y):
    """Short reason for a failure, found by a simple structural comparison."""
    x, y = walk(x, {}), walk(y, {})
    if isinstance(x, Var) or isinstance(y, Var):
        var, term = (x, y) if isinstance(x, Var) else (y, x)
        if occurs_in(var, term, {}):
            return f"occurs check: {var} occurs inside {term}"
    if isinstance(x, Compound) and isinstance(y, Compound):
        if x.functor != y.functor:
            return f"functor clash: {x.functor} vs {y.functor}"
        if len(x.args) != len(y.args):
            return f"arity clash: {x.functor}/{len(x.args)} vs {y.functor}/{len(y.args)}"
        for a, b in zip(x.args, y.args):
            if unify(a, b, {}) is None:
                return explain_failure(a, b)
        return "arguments conflict through shared variables"
    return f"clash: {x} and {y} are different and cannot be made equal"


def show_unification(text1, text2):
    """Unify two terms given as text and print the full result."""
    print(f"\nUnify  {text1}  and  {text2}")
    try:
        t1, t2 = parse_term(text1), parse_term(text2)
    except ValueError as error:
        print(f"   Input error: {error}")
        return
    subst = unify(t1, t2, {})
    if subst is None:
        print(f"   FAILURE ({explain_failure(t1, t2)})")
        return
    print("   SUCCESS. Most general unifier:")
    if not subst:
        print("      {}  (terms were already identical)")
    for var in sorted(subst, key=lambda v: v.name):
        print(f"      {var} = {resolve(var, subst)}")
    first, second = resolve(t1, subst), resolve(t2, subst)
    print(f"   After substitution both terms become: {first}")
    print(f"   Check (both sides identical): {first == second}")


DEMOS = [
    ("p(X, b)", "p(a, Y)"),
    ("f(X, g(Y))", "f(g(Z), X)"),
    ("knows(john, X)", "knows(Y, mother(Y))"),
    ("f(a, b)", "f(a, c)"),
    ("X", "f(X)"),
    ("f(a)", "g(a)"),
    ("f(a, b)", "f(a)"),
]


def main():
    print("=" * 60)
    print("EXPERIMENT 10: UNIFICATION ALGORITHM")
    print("=" * 60)
    print("Variables start with an UPPERCASE letter; constants/functors with lowercase.")
    print("\n--- Built-in demonstrations (successful and failed unification) ---")
    for first, second in DEMOS:
        show_unification(first, second)

    print("\n--- Try your own terms (press Enter on the first prompt to quit) ---")
    while True:
        first = ask("\nFirst term : ", "")
        if not first:
            break
        second = ask("Second term: ", "")
        if not second:
            break
        show_unification(first, second)
    print("\nDone.")


if __name__ == "__main__":
    main()
```

## Sample Input

The program first runs seven built-in examples (successful and failed). Afterwards you may type your own pair of terms, e.g. `q(X,X)` and `q(a,Z)`. Press Enter on the first prompt to quit.

## Expected Output

The outputs below were produced by actually running `main.py` (Python 3.12) with the inputs shown; text after each prompt is the input that was typed.

**Built-in demos, then user terms q(X,X) / q(a,Z) and a malformed term**

```text
============================================================
EXPERIMENT 10: UNIFICATION ALGORITHM
============================================================
Variables start with an UPPERCASE letter; constants/functors with lowercase.

--- Built-in demonstrations (successful and failed unification) ---

Unify  p(X, b)  and  p(a, Y)
   SUCCESS. Most general unifier:
      X = a
      Y = b
   After substitution both terms become: p(a, b)
   Check (both sides identical): True

Unify  f(X, g(Y))  and  f(g(Z), X)
   SUCCESS. Most general unifier:
      X = g(Z)
      Y = Z
   After substitution both terms become: f(g(Z), g(Z))
   Check (both sides identical): True

Unify  knows(john, X)  and  knows(Y, mother(Y))
   SUCCESS. Most general unifier:
      X = mother(john)
      Y = john
   After substitution both terms become: knows(john, mother(john))
   Check (both sides identical): True

Unify  f(a, b)  and  f(a, c)
   FAILURE (clash: b and c are different and cannot be made equal)

Unify  X  and  f(X)
   FAILURE (occurs check: X occurs inside f(X))

Unify  f(a)  and  g(a)
   FAILURE (functor clash: f vs g)

Unify  f(a, b)  and  f(a)
   FAILURE (arity clash: f/2 vs f/1)

--- Try your own terms (press Enter on the first prompt to quit) ---

First term : q(X,X)
Second term: q(a,Z)

Unify  q(X,X)  and  q(a,Z)
   SUCCESS. Most general unifier:
      X = a
      Z = a
   After substitution both terms become: q(a, a)
   Check (both sides identical): True

First term : f(a
Second term: f(a)

Unify  f(a  and  f(a)
   Input error: missing closing parenthesis

First term : 

Done.
```

## Result

Successful cases print the most general unifier and show both terms identical after substitution. Failures are reported with the reason (constant clash, functor clash, arity clash or occurs check). Malformed input is reported as an input error instead of crashing.

## How to Run

```bat
cd Experiment_10_Unification
python main.py
```

From the project root you can also run `run_experiment.bat 10`.
