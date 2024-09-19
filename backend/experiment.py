import os
from gptscholar.llm.base_llm import LlmSession
from gptscholar.llm.openai import OpenAiLlm
from gptscholar.kb.dblp import DblpKb
from gptscholar import GptScholar
from logging.config import dictConfig
from logger import Logger
import sys

dictConfig(
    {
        "version": 1,
        "disable_existing_loggers": True,
        "formatters": {
            "default": {
                "format": "[%(asctime)s] %(levelname)s in %(module)s: %(message)s",
            },
        },
        "handlers": {
            "console": {
                "level": "INFO",
                "class": "logging.StreamHandler",
                "formatter": "default",
                "stream": "ext://sys.stdout",
            },
            "file": {
                "class": "logging.handlers.RotatingFileHandler",
                "formatter": "default",
                "filename": "logs/experiment.log",
                "maxBytes": 31457280,
                "backupCount": 10,
                "delay": "True",
            },
        },
        "loggers": {
            "GPTscholar": {
                "handlers": [],
                "level": "DEBUG",
            },
        },
        "root": {
            "level": "DEBUG",
            "handlers": ["console", "file"],
        },
    }
)

chatgpt = OpenAiLlm(sys.argv[1])

gptscholar = GptScholar(
    llm = chatgpt,
    kb = DblpKb()
)

test_data = {
    "Get publications based on the author": [ 
        "Give me 3 papers authored by Wayne Xin Zhao.", 
        "Fetch me two papers authored by Leslie Lamport",
        "Give me 5 articles written by Dijkstra",
        "Zaojun Fang is an author. What are his papers?",
        "If I were to meet André Morim, what papers authored by him could I mention in a conversation to impress him?",
        "Give me just a single paper name in which Tim Berners-Lee participated.",
        "I really liked a paper I just read from Tom Heath. I wish to find others from him.",
        "I want to know more about Pedro Amorim. What papers did he write?",
        "I've been reading papers from Tom Brown. But I want to read even more papers from him. What is there to read?",
        "I heard that Mário S. Alvim is a reputable computer scientist. If that's true, he would likely have published some papers. I need examples to prove it.",
    ],
    "Get publications based on their domain": [ 
        "Give me articles about generative music.",
        "Give me papers about large language models.",
        "Give me publications that mention \"Information Retrieval\".",
        "I want to know more about \"Optimization\" through papers. Could you give me a list of concrete papers that could interest me?",
        "I am writing a literature review about reinforcement learning. What publications would you recommend?",
        "I am interested in \"Machine Learning\". Could you give me a list of papers about it?",
        "If I were researching about computer vision, what papers would you advise me to read?",
        "I intend to learn about deep learning. Which articles should I start reading?",
        "Cybersecurity is so fascinating, yet I know so little about it and don't know where to start. Could you give me a list of papers about it?",
        "My friend keeps talking about software engineering and wants me to discuss papers about it with him. I need to read some but can't find any. Could you help me?",
    ],
    "Get publications based on information from another publication": [ 
        "Give papers written by the same authors of \"From the Semantic Web to social machines: A research challenge for AI on the World Wide Web.\"",
        "Give me papers written in the same year as \"World-wide web: the information universe.\"",
        "Fetch me publications published in the same journal as \"Visual complexity of urban streetscapes: human vs computer vision.\"",
        "I want to know which other publications were published in ROBIO in year 2016 besides \"Modeling and diving control of a vector propulsion AUV\".",
        "Does Tim Berners-Lee published any paper in the same journal as \"Real-Time Piano Music Transcription Based on Computer Vision.\"? If so, give me 3 examples of them.",
        "Give me three papers similar to \"Visual complexity of urban streetscapes: human vs computer vision.\"",
        "I've read \"Training Compute-Optimal Large Language Models\". Great paper, thank you for the recommendation. Could you give me another paper writen by one the its authors?",
        "\"Towards Explaining Shortcut Learning Through Attention Visualization and Adversarial Attacks.\". Any other paper written by one of its authors?",
        "Composition and Perception in Spatial Audio.\nSuch a fascinating topic! Any other papers from the same journal?",
        "Towards Explaining Shortcut Learning Through Attention Visualization and Adversarial Attacks. I want to read more papers that talk about at least one of the same topics. Could you give me a list of them?",
    ],
    "Get publications based on their attributes": [ 
        "Give me papers published after the year 2000 by Leonard Adleman",
        "Retrieve articles from ROBIO published before the year 2018",
        "Is there any paper about \"Machine Learning\" published before the year 2019? Give me a list of them.",
        "I am interested in knowing if Leslie Lamport published any paper before the 80s. If so, what are they?",
        "I am interest in knowing more about the journal Computer Music Journal. What papers between 2010 and 2015 were published in it that you would recommend?",
        "Retrieve publications by Ashish Vaswani published no later than 2015.",
        "I am trying to find a publication whose DOI contains \"10.1109/ICRA.2016.7487220\". Could you help me?",
        "Is there any publication co-authored by Tom Heath and Tim Berners-Lee? If so, give me examples of publications.",
        "Does Ilke Kurt have any paper about COVID-19?",
        "Has Leslie Lamport published any publication about Robotics? List of them if possible.",
    ]
}

for case, prompts in test_data.items():
    for idx, prompt in enumerate(prompts):
        Logger().info(f"\n=========================================\nCase: {case}\nPrompt {idx}: {prompt}\n=========================================\n")
        base_folder = f"output/{case}/"
        if not os.path.exists(base_folder):
            os.makedirs(base_folder)

        # Baseline
        path_baseline = f"{base_folder}{idx}.baseline.txt"
        if os.path.exists(path_baseline):
            Logger().info(f"Skipping {path_baseline}...")
        else:
            baseline = LlmSession(chatgpt)
            result_baseline = baseline.prompt(prompt)
            with open(path_baseline, "w") as f:
                f.write(prompt)
                f.write("\n------------------\n")
                f.write(result_baseline)
        
        # GPTScholar
        path_gptscholar = f"{base_folder}{idx}.gptscholar.txt"
        if os.path.exists(path_gptscholar):
            Logger().info(f"Skipping {path_baseline}...")
        else:
            result_scholar = gptscholar.run(prompt)
            with open(path_gptscholar, "w") as f:
                f.write(prompt)
                f.write("\n------------------\n")
                f.write(result_scholar["final_response"])
