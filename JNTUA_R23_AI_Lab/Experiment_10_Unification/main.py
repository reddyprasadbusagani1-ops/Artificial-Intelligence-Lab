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
