import os
import random
import re

class WildcardNode():
    @classmethod
    def INPUT_TYPE(cls):
        data_in = {
            "required" : {
                "input_prompts" : ("STRING",)
            }
        }

        return data_in
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("output_prompts",)
    FUNCTION = "overridePrompt"
    CATEGORY = "🍮 Pururin777 Nodes"

    @staticmethod
    def checkPrompts(input_prompts):
        return re.findall("__([a-zA-Z])+(_([a-zA-Z])+)*([1-9][0-9]?)?__", input_prompts)

    @staticmethod
    def randomlySelect(wildcard):
        # Check if directory exists.
        if not os.path.exists("ComfyUI/custom_nodes/ComfyUI-Pururin777-Nodes/Wildcards/"):
            raise Exception("Error: There is no Wildcards folder!")
        
        # Check if directory is not empty.
        if len(os.listdir("ComfyUI/custom_nodes/ComfyUI-Pururin777-Nodes/Wildcards")) == 0:
            raise Exception("Error: There are no wildcard files!")
        
        match = re.search("([a-zA-Z])+(_([a-zA-Z])+)*([1-9][0-9]?)?", wildcard)
        file_name = match.group() + ".txt"
        possible_prompts = []
        prompt = ""

        with open("ComfyUI/custom_nodes/ComfyUI-Pururin777-Nodes/Wildcards/" + file_name, "r") as txt_file:
            # Check if the wildcard file is not empty.
            if not txt_file.read(1):
                raise Exception("Error: There are no values to choose from in the wildcard file!")
            
            while True:
                line = txt_file.readline()
                if not line:
                    break
                else:
                    possible_prompts.append(line)
        
        prompt = random.choice(possible_prompts)

        return prompt

    def overridePrompt(self, input_prompts):
        wildcards = WildcardNode.checkPrompts(input_prompts)
        output_prompts = input_prompts

        while wildcards:
            random_prompt = WildcardNode.randomlySelect(wildcards[0])
            output_prompts = output_prompts.replace(wildcards[0], random_prompt)
            wildcards = WildcardNode.checkPrompts(output_prompts)

        return (output_prompts,)
