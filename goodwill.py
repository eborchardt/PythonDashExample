import dash
from dash import html, dash_table
import requests

url = "https://buyerapi.shopgoodwill.com/api/Search/ItemListingData?pn=4&cl=1&cids=&scids=&p=1&sc=1&sd=false&cid=0&sg" \
      "=Keyword&st=celestron"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:129.0) Gecko/20100101 Firefox/129.0",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.5",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-site",
    "Pragma": "no-cache",
    "Cache-Control": "no-cache"
}


def get_data():
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()  # Assuming the response is in JSON format
        return data
    else:
        print(f"Error: {response.status_code}")
        return None


result = get_data()

if "searchResults" in result:
    print("Rendering search results")
    items = result["searchResults"]["items"]
    for item in items:
        item["itemUrl"] = f"https://shopgoodwill.com/item/{item['itemId']}"
        item["itemMDLink"] = f"[{item['title']}]({item['itemUrl']})"
        item["image"] = f"![{item['title']}]({item['imageURL']})"
    #     print_item_details(item)
else:
    print("No search results found. Perhaps the cosmos is keeping its secrets hidden.")

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Celestron Items Currently Accepting Bids"),
    dash_table.DataTable(
        id="item-grid",
        columns=[
            {"name": "Title", "id": "itemMDLink", "presentation": "markdown", "type": "text"},
            {"name": "Current Price", "id": "currentPrice"},
            {"name": "Remaining Time", "id": "remainingTime"},
            {"name": "Image", "id": "image", "presentation": "markdown"},
        ],
        data=items,
        style_table={"height": "90vh", "overflowY": "auto"},
        style_cell={
            "textAlign": "left",
            "padding": "10px",
            "whiteSpace": "normal",
            "height": "auto",
        },
        style_data={
            "width": "150px",
            "minWidth": "150px",
            "maxWidth": "150px",
            "overflow": "hidden",
            "textOverflow": "ellipsis",
        },
        markdown_options={"link_target": "_blank"},
    ),
])

if __name__ == "__main__":
    app.run_server(debug=True)
