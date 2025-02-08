from openai import OpenAI
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

def PromptCreator1(philosophy, gender, dream_type, relation1_l, relation2_l, relation3_l, description):
    dream_prompt = f"Interpret the following dream according to {philosophy} philosophy. "
    dream_prompt += f"I am a {gender}. "
    dream_prompt += f"I had a {dream_type[0]} dream. "
    

    # Add relation1 if available
    if relation1_l and len(relation1_l) > 0:
        dream_prompt += f"In my dream, I saw my {relation1_l[0]} "
        if len(relation1_l) > 1:
            dream_prompt += f"who is {relation1_l[1]} "
        if len(relation1_l) > 2:
            dream_prompt += f"and {relation1_l[2]}. "
        else:
            dream_prompt += ". "
    
    # Add relation2 if available
    if relation2_l and len(relation2_l) > 0:
        dream_prompt += f"In my dream, I also saw my {relation2_l[0]} "
        if len(relation2_l) > 1:
            dream_prompt += f"who is {relation2_l[1]} "
        if len(relation2_l) > 2:
            dream_prompt += f"and {relation2_l[2]}. "
        else:
            dream_prompt += ". "
    
    # Add relation3 if available
    if relation3_l and len(relation3_l) > 0:
        dream_prompt += f"In my dream, I also saw my {relation3_l[0]} "
        if len(relation3_l) > 1:
            dream_prompt += f"who is {relation3_l[1]} "
        if len(relation3_l) > 2:
            dream_prompt += f"and {relation3_l[2]}. "
        else:
            dream_prompt += ". "
    
    dream_prompt += f"{description}"
    
    return dream_prompt


def initialize (philosophy, gender, dream_type_l, relation1_l, relation2_l, relation3_l, description):
    client = OpenAI()
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a dream interpreter powered by AI."},
            {
                "role": "user",
                "content": PromptCreator1(philosophy, gender, dream_type_l, relation1_l, relation2_l, relation3_l, description)
            }
        ]
    )

    return completion.choices[0].message.content

# print(initialize("Buddhist", "Female", ["sexy"], ["boyfriend", "male", "alive"], "", "", "I despised the experience."))

@api_view(['GET', 'POST'])
def dream_interpretation(request):
    if request.method == 'GET':
        # Return some basic information about the API
        return Response({
            "message": "Dream Interpretation API",
            "usage": {
                "philosophy": "String - e.g., 'Buddhist', 'Freudian'",
                "gender": "String - e.g., 'Male', 'Female'",
                "dream_type": "List - e.g., ['scary']",
                "relation1": "List - e.g., ['mother', 'female', 'alive']",
                "relation2": "List - optional",
                "relation3": "List - optional",
                "description": "String - dream description"
            }
        })
    
    elif request.method == 'POST':
        try:
            # Extract data from request
            data = request.data
            philosophy = data.get('philosophy', '')
            gender = data.get('gender', '')
            dream_type = data.get('dream_type', [])
            relation1 = data.get('relation1', [])
            relation2 = data.get('relation2', [])
            relation3 = data.get('relation3', [])
            description = data.get('description', '')

            # Convert string values to lists if necessary
            if isinstance(dream_type, str):
                dream_type = [dream_type]
            if isinstance(relation1, str):
                relation1 = [relation1]
            if isinstance(relation2, str):
                relation2 = [relation2]
            if isinstance(relation3, str):
                relation3 = [relation3]

            # Validate required fields
            """
            if not all([philosophy, gender, dream_type, description]):
                return Response({
                    "error": "Missing required fields. Please provide philosophy, gender, dream_type, and description."
                }, status=status.HTTP_400_BAD_REQUEST)
            """

            # Call the initialize function

            interpretation = initialize(
                philosophy, 
                gender, 
                dream_type, 
                relation1, 
                relation2, 
                relation3, 
                description
            )

            return Response({
                "interpretation": interpretation
            }, status=status.HTTP_200_OK)

        except Exception as e:
            # Add more detailed error information
            return Response({
                "error": f"An error occurred: {str(e)}",
                "data_received": request.data
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)