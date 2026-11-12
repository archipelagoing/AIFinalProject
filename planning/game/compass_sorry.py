#!/usr/bin/env python3
"""Compass: Ship It — a tiny terminal race for completed GitHub issues."""

from __future__ import annotations

import json
import random
from dataclasses import asdict, dataclass, field
from pathlib import Path


TRACK_LENGTH = 40
CHECKPOINTS = {8: "Nov 12", 16: "Nov 14", 24: "Nov 19", 32: "Nov 21"}
SPACES = {
    3: ("Coffee Buff", "forward", 2),
    6: ("Merge Conflict", "back", 3),
    10: ("Pair Programming", "pair", 1),
    13: ("Clean CI Run", "forward", 3),
    18: ("GPU Timeout", "back", 4),
    21: ("Evidence Receipt", "shield", 1),
    26: ("Scope Creep", "reroll", 1),
    29: ("Works on My Machine", "back", 2),
    34: ("Demo Magic", "forward", 4),
    37: ("Production Bug", "skip", 1),
}


@dataclass
class Player:
    key: str
    name: str
    icon: str
    position: int = 0
    shields: int = 0
    skip_rolls: int = 0


@dataclass
class Game:
    players: list[Player] = field(default_factory=lambda: [
        Player("A", "Data + App", "A"),
        Player("B", "Finance + Wrapped", "B"),
        Player("C", "Model Lab", "C"),
        Player("D", "Conversation", "D"),
    ])
    passed_gates: list[int] = field(default_factory=list)
    log: list[str] = field(default_factory=list)
    completed_issues: list[str] = field(default_factory=list)

    def player(self, key: str) -> Player:
        for player in self.players:
            if player.key == key.upper():
                return player
        raise ValueError("Choose A, B, C, or D.")

    def can_finish(self) -> bool:
        return all(checkpoint in self.passed_gates for checkpoint in CHECKPOINTS)

    def move(self, player: Player, amount: int) -> None:
        destination = max(0, min(TRACK_LENGTH, player.position + amount))
        for checkpoint in sorted(CHECKPOINTS):
            if player.position < checkpoint <= destination and checkpoint not in self.passed_gates:
                player.position = checkpoint
                self.log.append(f"{player.key} reached the {CHECKPOINTS[checkpoint]} gate.")
                return
        if destination == TRACK_LENGTH and not self.can_finish():
            player.position = max(self.passed_gates, default=0)
            self.log.append(f"{player.key} needs every checkpoint before reaching FINISH.")
            return
        player.position = destination

    def resolve_space(self, player: Player, rng: random.Random) -> None:
        if player.position not in SPACES:
            return
        name, effect, amount = SPACES[player.position]
        if effect == "back" and player.shields:
            player.shields -= 1
            self.log.append(f"{player.key} used an Evidence Receipt against {name}.")
        elif effect == "forward":
            self.log.append(f"{player.key} landed on {name}: +{amount}.")
            self.move(player, amount)
        elif effect == "back":
            self.log.append(f"{player.key} landed on {name}: -{amount}.")
            self.move(player, -amount)
        elif effect == "shield":
            player.shields += amount
            self.log.append(f"{player.key} collected an Evidence Receipt.")
        elif effect == "skip":
            player.skip_rolls += amount
            self.log.append(f"{player.key} hit {name}: skip the next completed-issue roll.")
        elif effect == "reroll":
            bonus = rng.randint(1, 6)
            self.log.append(f"{player.key} hit {name}: bonus roll {bonus}.")
            self.move(player, bonus)
        elif effect == "pair":
            partners = [candidate for candidate in self.players if candidate.key != player.key]
            partner = min(partners, key=lambda candidate: candidate.position)
            self.move(player, amount)
            self.move(partner, amount)
            self.log.append(f"{player.key} paired with {partner.key}: both move +{amount}.")

    def complete_issue(self, key: str, issue_id: str, rng: random.Random) -> None:
        player = self.player(key)
        issue_id = issue_id.strip()
        if not issue_id:
            raise ValueError("Enter a GitHub issue ID or short title.")
        if issue_id in self.completed_issues:
            raise ValueError("That issue has already earned a roll.")
        self.completed_issues.append(issue_id)
        if player.skip_rolls:
            player.skip_rolls -= 1
            self.log.append(f"{player.key} completed {issue_id}, but skips this roll.")
            return
        roll = rng.randint(1, 6)
        self.move(player, roll)
        self.log.append(f"{player.key} completed {issue_id}, rolled {roll}, and moved to {player.position}.")
        self.resolve_space(player, rng)

    def pass_gate(self, checkpoint: int) -> None:
        if checkpoint not in CHECKPOINTS:
            raise ValueError("Choose an available checkpoint number.")
        if checkpoint not in self.passed_gates:
            self.passed_gates.append(checkpoint)
            self.passed_gates.sort()
            self.log.append(f"Team passed the {CHECKPOINTS[checkpoint]} checkpoint.")

    def winner(self) -> Player | None:
        return next((player for player in self.players if player.position >= TRACK_LENGTH), None)


def board(game: Game) -> str:
    occupants: dict[int, str] = {}
    for player in game.players:
        occupants[player.position] = occupants.get(player.position, "") + player.icon

    def cell(position: int) -> str:
        label = occupants.get(position, "") or ("G" if position in CHECKPOINTS else "·")
        return f"{position:02}{label:<2}"

    top = " ".join(cell(position) for position in range(0, 11))
    middle = []
    for left, right in zip(range(39, 30, -1), range(11, 20)):
        middle.append(f"{cell(left)}{' ' * 42}{cell(right)}")
    bottom = " ".join(cell(position) for position in range(30, 19, -1))
    return "\n".join([top, *middle, bottom, "START = 00   FINISH = 40"])


def show(game: Game) -> None:
    print("\n" + "=" * 62)
    print("             COMPASS: SHIP IT — ISSUE RACE")
    print("=" * 62)
    print(board(game))
    print("\nPlayers:")
    for player in game.players:
        status = []
        if player.shields:
            status.append(f"receipt x{player.shields}")
        if player.skip_rolls:
            status.append("skip next roll")
        print(f"  {player.key}  {player.name:<20} space {player.position:02}  {'; '.join(status) or 'ready'}")
    gates = ", ".join(CHECKPOINTS[gate] for gate in game.passed_gates) or "none"
    print(f"\nPassed gates: {gates}")
    if game.log:
        print("Latest: " + game.log[-1])


def save(game: Game, path: Path) -> None:
    path.write_text(json.dumps(asdict(game), indent=2) + "\n")


def load(path: Path) -> Game:
    raw = json.loads(path.read_text())
    return Game(players=[Player(**player) for player in raw["players"]],
                passed_gates=raw.get("passed_gates", []),
                log=raw.get("log", []),
                completed_issues=raw.get("completed_issues", []))


def prompt_gate(game: Game) -> None:
    pending = [checkpoint for checkpoint in CHECKPOINTS if checkpoint not in game.passed_gates]
    if not pending:
        print("All checkpoints already passed.")
        return
    print("Pending gates: " + ", ".join(f"{checkpoint} ({CHECKPOINTS[checkpoint]})" for checkpoint in pending))
    answer = input("Pass which gate? ").strip()
    game.pass_gate(int(answer))


def main() -> None:
    root = Path(__file__).resolve().parent
    save_path = root / "saves" / "compass_ship_it.json"
    save_path.parent.mkdir(exist_ok=True)
    game = load(save_path) if save_path.exists() else Game()
    rng = random.Random()
    print("Complete a real GitHub issue with evidence, then record its roll here.")
    print("Commands: [i]ssue, [g]ate, [s]ave, [l]og, [r]eset, [q]uit")
    while not game.winner():
        show(game)
        command = input("\n> ").strip().lower()
        try:
            if command in {"i", "issue"}:
                key = input("Player (A/B/C/D): ").strip()
                issue_id = input("Accepted GitHub issue ID/title: ").strip()
                confirmed = input("Code, test, and evidence accepted? [y/N] ").strip().lower()
                if confirmed == "y":
                    game.complete_issue(key, issue_id, rng)
                else:
                    print("No roll until the issue evidence is accepted.")
            elif command in {"g", "gate"}:
                prompt_gate(game)
            elif command in {"s", "save"}:
                save(game, save_path)
                print(f"Saved to {save_path.name}.")
            elif command in {"l", "log"}:
                print("\n".join(game.log[-12:]) or "No events yet.")
            elif command in {"r", "reset"}:
                if input("Reset the game? [y/N] ").strip().lower() == "y":
                    game = Game()
                    save(game, save_path)
            elif command in {"q", "quit"}:
                save(game, save_path)
                return
            else:
                print("Choose i, g, s, l, r, or q.")
        except (ValueError, json.JSONDecodeError) as error:
            print(f"Not applied: {error}")
        save(game, save_path)
    show(game)
    print(f"\n🏆 {game.winner().name} wins Compass: Ship It!")
    save(game, save_path)


if __name__ == "__main__":
    main()
