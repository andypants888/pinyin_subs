import pysrt

def main(input_file):
    # with open(input_file, "r") as f:
    #     content = f.read()
    subs = pysrt.open(input_file)


    print(subs[1])

    print("Hello from pinyinsubs!")




if __name__ == "__main__":
    main("resources/How.To.S01E01._en_tiny.srt")
