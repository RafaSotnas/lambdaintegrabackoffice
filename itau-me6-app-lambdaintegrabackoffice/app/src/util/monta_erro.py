def payload_erro(erros: list, resource_name: str) -> dict:

    msg = {
        "controle": "erro",
        "Resource": "lambda",
        "ResourceName": f"{resource_name}",
        "Erros": [],
    }

    msg["Erros"].append(erros)

    return msg
