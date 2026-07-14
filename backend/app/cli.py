"""Piece 6 (CLI): a terminal loop so you can actually play the game."""
from app.game import run_turn

SESSION = "cli-session"  # same id every turn = the campaign remembers itself


def main():
    print("=" * 60)
    print("  DUNGEONS & DRAGONS - AI Game Master")
    print("  Type your action each turn. Type 'quit' to exit.")
    print("=" * 60)

    while True:
        player_input = input("\n> ").strip()
        if player_input.lower() in {"quit", "exit"}:
            print("Farewell, adventurer!")
            break
        if not player_input:
            continue

        print("\n(the Game Master considers...)\n")
        turn = run_turn(player_input, SESSION)

        print(turn.narrative)
        if turn.dice:
            print(f"\n[Dice: {turn.dice}]")
        if turn.suggested_actions:
            print("\nYou could:")
            for i, action in enumerate(turn.suggested_actions, 1):
                print(f"  {i}. {action}")


if __name__ == "__main__":
    main()