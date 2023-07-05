import asyncio
import os
from datetime import datetime

import vaex as vaex
from loguru import logger
from dadata import DadataAsync
import csv
import httpx
import httpcore


main_data = 'db_name.csv'
dump = 'also_db_name.csv'

df_main = vaex.from_csv(main_data, low_memory=False)
df_dump = vaex.from_csv(dump, low_memory=False)

# Parsing column 'inn'
inn_column_main = df_main['ИНН']
inn_column_dump = df_dump['inn']

# Column to NumPy
np_main = inn_column_main.to_numpy()
np_dump = inn_column_dump.to_numpy()

# Main async function
async def fetch_data(number):
    token = "your_token"
    secret = "your_secret"
    # Open context manager
    async with DadataAsync(token, secret) as dadata:

        async with request_semaphore:
            inn = str(number)
            # Make a flag in case of an error
            got_response = False
            while not got_response:
                try:
                    result = await dadata.find_by_id("party", str(inn), count=1, branch_type='MAIN',
                                                     status='ACTIVE',
                                                     timeout=120)
                    await asyncio.sleep(1)
                    got_response = True
                # Error handler
                except httpx.ConnectTimeout as e:
                    logger.error(f"Connection timeout: {e}")
                    continue
                except httpcore.RemoteProtocolError as e:
                    logger.error("RemoteProtocolError: {e}. Продолжаем работу.")
                    continue
                except httpx.RemoteProtocolError as e:
                    logger.error(e)
                    continue

        if result == []:
            logger.info(f'{inn}: Null: ' + inn)

        else:
            data = {
                'Inn': inn,
                'Data': result[0]['data']
            }

            logger.info(f'{inn}: Got data for inn: ' + inn)
            with open(csv_file_path, 'a', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=data.keys())
                if file.tell() == 0:
                    writer.writeheader()
                writer.writerow(data)


async def main():
    tasks = []
    for i in np_main:
        if check_inn_in_table(i):
            logger.warning(f"{i}: already in csv table.")
            continue
        task = asyncio.create_task(fetch_data(i))
        tasks.append(task)

    await asyncio.gather(*tasks)

# Check if such value already exists
def check_inn_in_table(inn):
    return (np_dump == inn).any()


def create_csv_file():
    directory = "./data/individual_data"
    if not os.path.exists(directory):
        os.makedirs(directory)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{directory}/data_{timestamp}_individual.csv"

    return filename


csv_file_path = create_csv_file()
# To avoid request limit use 5 workers
request_semaphore = asyncio.Semaphore(5)
asyncio.run(main())
