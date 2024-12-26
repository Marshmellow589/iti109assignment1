from dotenv import load_dotenv
import os

# Import namespaces
# import namespaces
from azure.core.credentials import AzureKeyCredential
from azure.ai.language.questionanswering import QuestionAnsweringClient
# import namespaces
from azure.ai.translation.text import *
from azure.ai.translation.text.models import InputTextItem

def main():
    try:
        # Get Configuration Settings
        load_dotenv()
        ai_endpoint = os.getenv('AI_SERVICE_ENDPOINT')
        ai_key = os.getenv('AI_SERVICE_KEY')
        ai_project_name = os.getenv('QA_PROJECT_NAME')
        ai_deployment_name = os.getenv('QA_DEPLOYMENT_NAME')
        tr_ai_endpoint = os.getenv('trans_endpoint')
        tr_ai_key = os.getenv('trans_key')

        # Create client using endpoint and key
        # Initialize the Translator clienthello
        credential = TranslatorCredential(tr_ai_key, 'eastus')
        client = TextTranslationClient(tr_ai_endpoint)
 
        # Create client using endpoint and key
        credential = AzureKeyCredential(ai_key)
        ai_client = QuestionAnsweringClient(endpoint=ai_endpoint, credential=credential)
        #translateion_function
        def translation(inputtext,target_language):
            input_text_elements = [InputTextItem(text=inputtext)]
            translationResponse = client.translate(content=input_text_elements, to=[target_language])
            translation = translationResponse[0] if translationResponse else None
            if translation:
                sourceLanguage = translation.detected_language
                for translated_text in translation.translations:
                    print(f"'{inputtext}' was translated from {sourceLanguage.language} to {translated_text.to} as '{translated_text.text}'.")

        # Submit a question and display the answer
        user_question = ''
        while user_question.lower() != 'quit':
            user_question = input('\nQuestion:\n')
            response = ai_client.get_answers(question=user_question,
                                            project_name=ai_project_name,
                                            deployment_name=ai_deployment_name)
            for candidate in response.answers:
                print(candidate.answer)
                print("Confidence: {}".format(candidate.confidence))
                print("Source: {}".format(candidate.source))
                print(translation(candidate.answer,'es')) #spanish




    except Exception as ex:
        print(ex)


if __name__ == "__main__":
    main()
