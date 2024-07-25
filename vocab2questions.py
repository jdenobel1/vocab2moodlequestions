import xml.etree.ElementTree as ET
import os

# Ensure the file path is correct | enter the file path location
file_path = ''

try:
    tree = ET.parse(file_path)
    root = tree.getroot()

    # Initialize a dictionary to hold the data
    glossary_data = {}

    # Extract data from the XML
    for entry in root.findall(".//ENTRY"):
        concept = entry.find("CONCEPT").text
        definition = entry.find("DEFINITION").text
        category = entry.find(".//CATEGORY/NAME").text

        if category not in glossary_data:
            glossary_data[category] = []

        glossary_data[category].append((definition, concept))

    # Function to generate Aiken format questions
    def generate_aiken_questions(glossary_data):
        questions_by_unit = {}
        for unit, items in glossary_data.items():
            questions = []
            for index, (definition, concept) in enumerate(items):
                # Select incorrect options randomly from the same unit
                incorrect_options = [c for d, c in items if c != concept]
                if len(incorrect_options) >= 3:
                    incorrect_options = incorrect_options[:3]
                else:
                    incorrect_options.extend(['Dummy1', 'Dummy2', 'Dummy3'][:3-len(incorrect_options)])
                
                # Shuffle options
                import random
                options = incorrect_options + [concept]
                random.shuffle(options)
                correct_answer = options.index(concept)

                question_text = f"{index + 1}. {definition}\n"
                for i, option in enumerate(options):
                    question_text += f"{chr(65+i)}. {option}\n"
                question_text += f"ANSWER: {chr(65+correct_answer)}\n"
                questions.append(question_text)
            questions_by_unit[unit] = questions
        return questions_by_unit

    # Generate the questions
    aiken_questions_by_unit = generate_aiken_questions(glossary_data)

    # Directory to save the questions
    output_dir = 'C:/Users/jdeno/Desktop/Adobe_video/vocab_questions'

    # Ensure the directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Export each unit's questions to a separate text file
    for unit, questions in aiken_questions_by_unit.items():
        file_name = f'vocab_question_{unit.replace(" ", "_").lower()}.txt'
        file_path = os.path.join(output_dir, file_name)
        with open(file_path, 'w') as file:
            for question in questions:
                file.write(question + "\n")
        print(f"Questions for {unit} saved to {file_path}")

except FileNotFoundError:
    print(f"File not found: {file_path}")
except ET.ParseError:
    print(f"Error parsing the XML file: {file_path}")
except Exception as e:
    print(f"An error occurred: {e}")
