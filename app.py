from dotenv import load_dotenv
from src import main
import asyncio

load_dotenv()


if __name__ == "__main__":
    asyncio.run(main())
