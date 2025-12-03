import json
import sys
import asyncio
from xmlconvert import xml_to_json

try:
    import eywa
except Exception:
    print("EYWA SDK nije dostupan. Pokreni kroz 'eywa run -c ...' ili instaliraj SDK.", file=sys.stderr)
    sys.exit(2)

MUTATION = """
mutation insertManyOrderHeaders($data:[OrderHeaderInput!]) {
  stackOrderHeaderList(data:$data) {
    client {
      client_id
      delivery_point
      username
      password
    }
    requests {
      atk
      ean
      article_number
      order_quantity
    }
    reference_number
    document_date
  }
}
"""

def prepare_payload(json_data: str):

    data = json.loads(json_data)

    orders = data["Orders"]["OrderRequest"]

    payload = []

    for order in orders:
        header = order["OrderHeader"]
        client = header["ClientInformation"]

        lines = order["OrderLine"]["RequestOrderLine"]

        formatted = {
            "client": {
                "client_id": client.get("ClientID"),
                "delivery_point": client.get("DeliveryPoint"),
                "username": client.get("Username"),
                "password": client.get("Password")
            },
            "reference_number": header.get("ReferenceNumber"),
            "document_date": header.get("DocumentDate"),
            "requests": []
        }
        for line in lines:
            formatted["requests"].append({
                "atk": line.get("ATK"),
                "ean": line.get("EAN"),
                "article_number": line.get("ArticleNumber"),
                "order_quantity": line.get("OrderQuantity")
            })

        payload.append(formatted)

    return payload

async def send_to_db(data):

    gql = await eywa.graphql(
        MUTATION,
        variables={"data": data}
    )

    eywa.info("RESPONSE FROM EYWA:")
    eywa.info(gql)

    return gql

async def main():
    eywa.open_pipe()

    eywa.info("Converting XML → JSON ...")
    json_data = xml_to_json("Oktal-farma.xml", "Oktal-farma.json")

    eywa.info("Preparing payload ...")
    payload = prepare_payload(json_data)

    eywa.info(f"Sending {len(payload)} orders to EYWA ...")
    await send_to_db(payload)

    eywa.exit()

if __name__ == "__main__":
    asyncio.run(main())