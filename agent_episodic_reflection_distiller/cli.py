"""CLI for agent-episodic-reflection-distiller."""
import argparse
import sys
from .core import ReflectionDistiller, TrajectorySummary

def main():
    parser = argparse.ArgumentParser(description="Agent Episodic Reflection Distiller CLI")
    parser.add_argument("--demo", action="store_true", help="Run episodic reflection distillation demo")
    args = parser.parse_args()

    if args.demo:
        distiller = ReflectionDistiller()
        t1 = TrajectorySummary("s1", False, ["start_server"], "Error: Address already in use on port 8080")
        t2 = TrajectorySummary("s2", False, ["write_config"], "Permission denied: /etc/nginx/nginx.conf")

        rules = distiller.distill([t1, t2])
        print(f"[+] Distilled {len(rules)} actionable procedural heuristics:")
        for r in rules:
            print(f"    IF {r.condition} -> THEN {r.recommendation} (conf={r.confidence:.2f})")
    else:
        parser.print_help()
    sys.exit(0)

if __name__ == "__main__":
    main()
