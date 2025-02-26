def main(input_srt):
    with open(input_srt, "r") as f:
        content = f.read()

    print(content)

    print("Hello from pinyinsubs!")



if __name__ == "__main__":
    main("resources/How.To.S01E01._en_tiny.srt")
