# Load the text file
with open("slurm-5163884.out", "r", encoding='utf-8') as file:
    content = file.read()

chunks = content.split("Reponse took")
print(len(chunks))

print(chunks[182])
