import json
from datetime import datetime

from app.database.models import Participant, Process, ProcessDetail, Proceeding


async def load_initial_data():
    is_empty = await Participant.all().count() == 0
    if is_empty:
        print("Database is empty, loading initial data...")
        print("This process may take a few minutes, please wait...")

        # * Get initial data from json file
        data: list = []
        with open("./app/database/fixtures/initial_data.json", "r", encoding="utf-8") as file:
            data = json.load(file)

        # * Create participants
        for participant_data in data:
            participant = await Participant.create(
                type=participant_data["type"],
                identifier=participant_data["identifier"],
                process_count=participant_data["process_count"],
            )

            # * Load processes
            processes: list[dict] = participant_data["processes"]
            for process_data in processes:
                process_date = datetime.strptime(process_data["date"], "%d/%m/%Y").strftime("%Y-%m-%d")
                process = await Process.create(
                    process_id=process_data["id"],
                    date=process_date,
                    number=process_data["process_number"],
                    infringement=process_data["infringement"],
                    participant=participant,
                )

                # * Load process details
                process_details: list[dict] = process_data["process_details"]
                for process_detail_data in process_details:
                    process_detail_date = datetime.strptime(process_detail_data["date"], "%d/%m/%Y %H:%M").strftime(
                        "%Y-%m-%d %H:%M"
                    )
                    process_detail = await ProcessDetail.create(
                        dependency=process_detail_data["dependency"],
                        city=process_detail_data["city"],
                        number=process_detail_data["number"],
                        date=process_detail_date,
                        actors=process_detail_data["actors"],
                        defendants=process_detail_data["defendants"],
                        process=process,
                    )

                    # * Load proceedings
                    proceedings: list[dict] = process_detail_data["proceedings"]
                    for proceeding_data in proceedings:
                        proceeding_date = datetime.strptime(proceeding_data["date"], "%d/%m/%Y %H:%M").strftime(
                            "%Y-%m-%d %H:%M"
                        )
                        proceeding = await Proceeding.create(
                            date=proceeding_date,
                            title=proceeding_data["title"],
                            content=proceeding_data["content"],
                            process_detail=process_detail,
                        )

            print(f"Participant {participant.identifier} created successfully")
    else:
        print("Database is not empty, skipping initial data loading...")
