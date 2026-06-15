import random


groups = {
	"Group A": ["Portugal", "Spain", "England", "Netherlands"],
	"Group B": ["Argentina", "Brazil", "France", "Germany"],
}

team_strength = {
	"Portugal": 9,
	"Spain": 7,
	"England": 7,
	"Netherlands": 6,
	"Argentina": 8,
	"Brazil": 7,
	"France": 7,
	"Germany": 6,
}

attempts = 0


def generate_goals(team):
	return random.randint(0, 2) + (1 if random.randint(1, 10) <= team_strength[team] else 0)


def play_group_match(team1, team2):
	team1_goals = generate_goals(team1)
	team2_goals = generate_goals(team2)
	print(f"{team1} {team1_goals} - {team2_goals} {team2}")
	return team1_goals, team2_goals


def build_group_fixtures(group_teams):
	return [
		[(group_teams[0], group_teams[1]), (group_teams[2], group_teams[3])],
		[(group_teams[0], group_teams[2]), (group_teams[1], group_teams[3])],
		[(group_teams[0], group_teams[3]), (group_teams[1], group_teams[2])],
	]


def play_knockout_match(team1, team2):
	team1_goals = generate_goals(team1)
	team2_goals = generate_goals(team2)
	print(f"{team1} {team1_goals} - {team2_goals} {team2}")

	while team1_goals == team2_goals:
		print("The match is tied, so it goes to extra time.")
		team1_goals += random.randint(0, 1)
		team2_goals += random.randint(0, 1)

		# Force a result if extra time also ends level (penalty shootout)
		if team1_goals == team2_goals:
			print("Still tied after extra time. Going to penalties.")
			if random.randint(0, 1) == 0:
				team1_goals += 1
			else:
				team2_goals += 1

	if team1_goals > team2_goals:
		return team1
	return team2


def run_group_stage():
	qualified_teams = []

	for group_name, group_teams in groups.items():
		print(f"\n{group_name}")
		points = {team: 0 for team in group_teams}
		fixtures = build_group_fixtures(group_teams)

		for matchday_number, matchday in enumerate(fixtures, start=1):
			print(f"Matchday {matchday_number}")
			for team1, team2 in matchday:
				team1_goals, team2_goals = play_group_match(team1, team2)

				if team1_goals > team2_goals:
					points[team1] += 3
				elif team2_goals > team1_goals:
					points[team2] += 3
				else:
					points[team1] += 1
					points[team2] += 1

		group_ranking = sorted(group_teams, key=lambda team: (points[team], team_strength[team]), reverse=True)
		print("Group standings:")
		for team in group_ranking:
			print(f"{team}: {points[team]} points")

		qualified_teams.append(group_ranking[0])
		qualified_teams.append(group_ranking[1])

	return qualified_teams


def run_knockout_stage(qualified_teams):
	print("\nKnockout Stage")
	semi_final_1_winner = play_knockout_match(qualified_teams[0], qualified_teams[3])
	semi_final_2_winner = play_knockout_match(qualified_teams[1], qualified_teams[2])
	print("\nFinal")
	champion = play_knockout_match(semi_final_1_winner, semi_final_2_winner)
	return champion


print("World Cup 2026 Simulation")
print("Type 'start' to begin, 'skip' to pass, or 'quit' to stop.")

while True:
	user_input = input("Enter your choice: ").strip().lower()

	if user_input == "quit":
		print("Simulation stopped.")
		break

	elif user_input == "skip":
		pass
		print("You skipped this round.")
		continue

	elif user_input == "start":
		attempts += 1
		print(f"Round {attempts}: Starting a mini World Cup simulation.")
		qualified_teams = run_group_stage()
		winner_country = run_knockout_stage(qualified_teams)
		print(f"{winner_country} wins the World Cup 2026 simulation!")
		break

	else:
		print("Invalid input. Type 'start', 'skip', or 'quit'.")
		continue