import pysrt

import os
from dotenv import load_dotenv
load_dotenv()

from openai import OpenAI

# For chatgpt
# client = OpenAI()

# For deepseek
deepseek_key = os.getenv("api_key")
client = OpenAI(api_key=deepseek_key, base_url="https://api.deepseek.com")

import re

# Allow help() print to terminal
# import pydoc

# Original help
# help(client)

# Hard string
# print(pydoc.render_doc(client))

def main(input_file, output_file):
    # with open(input_file, "r") as f:
    #     content = f.read()
    subs_original = pysrt.open(input_file)
    subs_chinese = []
    subs_pinyin = []

    # Translate & Push to List
    # To do: cache the translation outputs
    for i in range(0, len(subs_original), 1):
        print(f"{i}-------")

        single_clean_subtitle = remove_html(subs_original[i].text).replace("\n", " ")

        # help(subs_original[i])
        print(subs_original[i].index)
        print(subs_original[i].start)
        print(subs_original[i].end)
        print(single_clean_subtitle)
        print(subs_original[i].position)
        # print(single_clean_subtitle)

        # Translate
        single_chinese_sub = translate_deepseek(single_clean_subtitle, "Simplified Chinese")
        # subs_chinese.append(single_chinese_sub)
        print(single_chinese_sub)
        single_pinyin_sub = translate_deepseek(single_chinese_sub, "Pinyin")
        print(single_pinyin_sub)
        # subs_pinyin.append(single_pinyin_sub)

        # Write new output srt file
        with open(output_file, "a") as file:
            file.write(f"{subs_original[i].index}\n")
            file.write(f"{subs_original[i].start} --> {subs_original[i].end}\n")
            file.write(f"{single_chinese_sub}\n")
            file.write(f"{add_styling_html(single_pinyin_sub, '<font size="11">', '</font>')}\n")
            file.write(f"{add_styling_html(single_clean_subtitle, '<font size="11">', '</font>')}\n")
            file.write(f"\n")

    
        

    # for subtitle in subs_original:
    #     print(subtitle.text)
    #     print("---")

    # print(subs_original[1].text)
    # help(subs_original[0])
    # print("Hello from pinyinsubs!")

def remove_html(text):
    clean_regex_obj = re.compile("<.*?>")
    return re.sub(clean_regex_obj, "", text)

def add_styling_html(text, opening_tag, closing_tag):
    return f"{opening_tag}{text}{closing_tag}"


def translate_openai(original_text, output_language):
    # Small
    # model="gpt-4o-mini",

    # Medium
    # model="gpt-4",
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {
                "role": "user",
                "content": f"Translate '{original_text}' to {output_language}. Remove any HTML tags like <i> Return the output without any explanation or extra text. MAKE SURE THE TRANSLATION IS LIKE A NATIVE SPEAKER, AVOID TRANSLATING TOO DIRECTLY."
            }
        ]
    )

    # Debug
    # print(completion.choices[0].message)
    # print(completion.choices[0].message.content)

    return completion.choices[0].message.content

# build-success/gpt-4-full-ep01-s1-how-to.srt
# fix 527 low-key
# fix 316 inaudible
# fix 59
def translate_deepseek(original_text, output_language):
    completion = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": f"""You are a translator. You will be translating the original subtitle to {output_language}. Return the output without any explanation or extra text. MAKE SURE THE TRANSLATION IS LIKE A NATIVE SPEAKER, AVOID TRANSLATING TOO DIRECTLY. 
             
            WATCH OUT FOR THE FOLLOWING TRANSLATION MISTAKES:
             - translating proper names like 'WrestleMania' to '摔角狂热', Instead opting for the original name, 'WrestleMania'
             - attempting interpret text like 'INAUDIBLE', this subtitle is for hearing-impaired persons and should be translated
             - translating english expressions like 'Probably low-key why I am out here' into '低调的原因', instead, finding an NATIVE IDIOM or EXPRESSION that matches the emotion of the original
             
             A Good translation was:
             '你觉得人类会东山再起吗? Do you think Mankind is gonna make a comeback?' because the translation of comeback was very appropriate as an expression into Chinese
             """},
            {
                "role": "user",
                "content": f"Translate '{original_text}' to {output_language}. "
            }
        ],
        stream=False
    )

    # Debug
    # print(completion.choices[0].message)
    print("DEEPSEEK: ", completion.choices[0].message.content)

    return completion.choices[0].message.content
    



if __name__ == "__main__":
    # main("S01E05/How.To.with.John.Wilson.S01E05.AMZN.WEBRip.DDP5.1.x264-NTb_HI.en.srt", "new_file.srt")
    main("dev-test/S03E04_10_lines.srt", "new_file.srt")
    # main("resources/How.To.S01E01._en_origin.srt")
    # translate_openai("HELLO ANDREW!", "Simplified Chinese")
