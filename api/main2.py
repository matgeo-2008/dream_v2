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
            # Try to get data from either POST body or query parameters
            data = request.data if request.data else request.query_params
            
            # Clean the data - remove quotes from string values
            philosophy = data.get('philosophy', '').strip('"')
            gender = data.get('gender', '').strip('"')
            
            # Handle dream_type list
            dream_type = data.get('dream_type', '[]')
            if isinstance(dream_type, str):
                dream_type = dream_type.strip('[]').replace('"', '').split(',')
                dream_type = [item.strip() for item in dream_type if item.strip()]
            
            # Handle relation lists
            def parse_relation(rel_str):
                if not rel_str or rel_str == '[]':
                    return []
                if isinstance(rel_str, str):
                    rel_str = rel_str.strip('[]').replace('"', '').split(',')
                    return [item.strip() for item in rel_str if item.strip()]
                return rel_str

            relation1 = parse_relation(data.get('relation1', '[]'))
            relation2 = parse_relation(data.get('relation2', '[]'))
            relation3 = parse_relation(data.get('relation3', '[]'))
            
            description = data.get('description', '').strip('"')

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
                "data_received": {
                    "query_params": request.query_params,
                    "body": request.data
                }
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)