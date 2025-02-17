from src.Program import Program
from src.settings import create_tables

if __name__ == "__main__":
    program = Program()
    create_tables()
    program.main()
