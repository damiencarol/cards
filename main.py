
import cards

def main():
    print("launching tests...")

    from tests.test_cards import test_load
    test_load()


if __name__ == "__main__":
    main()
