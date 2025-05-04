import openai

def generate_report(data, report_type):
    prompt = f"""
    Gere um relatório de {report_type} para engenharia ambiental com os dados:
    {data}.
    Use termos técnicos e cite normas como CONAMA 357/05.
    """
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content