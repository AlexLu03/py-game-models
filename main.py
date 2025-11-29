import init_django_orm  # noqa: F401
import json
from db.models import Race, Skill, Player, Guild


def main() -> None:
    with open("players.json") as d:
        players_data = json.load(d)
        for nickname, p_data in players_data.items():
            race, _ = Race.objects.get_or_create(
                name=p_data["race"]["name"],
                defaults={"description": p_data["race"]["description"]}
            )

            guild_data = p_data.get("guild")
            if guild_data:
                guild, _ = Guild.objects.get_or_create(
                    name=guild_data.get("name"),
                    defaults={"description": guild_data.get("description")}
                )
            else:
                guild = None

            for skill_data in p_data.get("race", {}).get("skills", []):
                skill, _ = Skill.objects.get_or_create(
                    name=skill_data.get("name"),
                    race=race,
                    defaults={"bonus": skill_data.get("bonus")}
                )

            Player.objects.create(
                nickname=nickname,
                email=p_data.get("email"),
                bio=p_data.get("bio"),
                race=race,
                guild=guild
            )


if __name__ == "__main__":
    main()
