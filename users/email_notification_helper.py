import os
import smtplib
from email.mime.text import MIMEText

from dotenv import load_dotenv

load_dotenv()

SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = 587
SMTP_USERNAME = os.getenv("SMTP_USERNAME")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")

SENDER_EMAIL = os.getenv("SMTP_USERNAME")


def send_email(
        order: dict,
        recipient_email: str
) -> None:
    try:
        smtp_server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)

        smtp_server.starttls()

        smtp_server.login(SMTP_USERNAME, SMTP_PASSWORD)

        product_html = make_products_html(
            order.get("products")
        )

        body = f"""
        <html>
          <body>
            <div>
                <h3>This is your order detail</h3>
                <ul>{product_html}</ul>
                <p><b>Total price:<b> {order.get("total_price")}$</p>
                <p><b>Link to pay:<b> {order.get("payment_url")}</p>
            </div>
          </body>
        </html>
        """

        msg = MIMEText(body, "html")
        msg["From"] = SENDER_EMAIL
        msg["To"] = recipient_email
        msg["Subject"] = "Order detail from ProductManagementAPI"

        smtp_server.sendmail(
            SENDER_EMAIL, recipient_email, msg.as_string()
        )

        smtp_server.quit()

    except Exception:
        pass


def make_products_html(products: list) -> str:
    product_html = """"""

    for product in products:
        product_html += f"""
            <li>
                <b>{product.get("name")}</b><br>
                Price: {product.get("price")}$<br>
                Quantity: {product.get("quantity")}
            </li>
        """

    return product_html

