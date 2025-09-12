"""
Appwrite Function: Send Email
Handles email delivery for generated flyers
"""
import json
import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import base64
from typing import Dict, Any


def main(context):
    """
    Send email with flyer attachment
    Expected payload:
    {
        "to": "recipient@example.com",
        "subject": "Happy Birthday!",
        "htmlBody": "<html>...",
        "textBody": "Plain text version",
        "flyerBase64": "base64_encoded_image",
        "flyerFilename": "birthday_flyer.png"
    }
    """
    try:
        # Parse input
        payload = json.loads(context.req.body)

        # Required fields
        to_email = payload.get('to')
        subject = payload.get('subject')
        html_body = payload.get('htmlBody')

        if not all([to_email, subject, html_body]):
            return context.res.json({
                'success': False,
                'error': 'Missing required fields: to, subject, htmlBody'
            }, 400)

        # Optional fields
        text_body = payload.get('textBody', '')
        flyer_base64 = payload.get('flyerBase64')
        flyer_filename = payload.get('flyerFilename', 'flyer.png')

        # Send email
        result = send_email(
            to_email=to_email,
            subject=subject,
            html_body=html_body,
            text_body=text_body,
            flyer_base64=flyer_base64,
            flyer_filename=flyer_filename
        )

        if result['success']:
            return context.res.json({
                'success': True,
                'message': 'Email sent successfully',
                'messageId': result.get('messageId')
            })
        else:
            return context.res.json({
                'success': False,
                'error': result['error']
            }, 500)

    except Exception as e:
        return context.res.json({
            'success': False,
            'error': f'Function error: {str(e)}'
        }, 500)


def send_email(to_email: str, subject: str, html_body: str, text_body: str = '',
               flyer_base64: str = None, flyer_filename: str = 'flyer.png') -> Dict[str, Any]:
    """
    Send email using SMTP
    """
    try:
        # Email configuration from environment variables
        smtp_server = os.environ.get('SMTP_SERVER', 'smtp.gmail.com')
        smtp_port = int(os.environ.get('SMTP_PORT', '587'))
        smtp_username = os.environ.get('SMTP_USERNAME')
        smtp_password = os.environ.get('SMTP_PASSWORD')
        from_email = os.environ.get('FROM_EMAIL', smtp_username)
        from_name = os.environ.get('FROM_NAME', 'Drawtab')

        if not all([smtp_username, smtp_password]):
            return {'success': False, 'error': 'SMTP credentials not configured'}

        # Create message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = f"{from_name} <{from_email}>"
        msg['To'] = to_email

        # Add text and HTML parts
        if text_body:
            text_part = MIMEText(text_body, 'plain')
            msg.attach(text_part)

        html_part = MIMEText(html_body, 'html')
        msg.attach(html_part)

        # Add flyer attachment if provided
        if flyer_base64:
            try:
                flyer_data = base64.b64decode(flyer_base64)
                flyer_attachment = MIMEImage(flyer_data)
                flyer_attachment.add_header(
                    'Content-Disposition',
                    f'attachment; filename="{flyer_filename}"'
                )
                msg.attach(flyer_attachment)
            except Exception as e:
                print(f"Error attaching flyer: {e}")

        # Send email
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)

        message_id = server.send_message(msg)
        server.quit()

        return {
            'success': True,
            'messageId': message_id
        }

    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }


def generate_birthday_email_template(name: str, age: int = None) -> Dict[str, str]:
    """
    Generate birthday email template
    """
    subject = f"🎉 Happy Birthday, {name}!"

    html_body = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>Happy Birthday!</title>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; border-radius: 10px; }}
            .content {{ padding: 30px 20px; background: #f9f9f9; border-radius: 10px; margin: 20px 0; }}
            .footer {{ text-align: center; color: #666; padding: 20px; }}
            .flyer {{ text-align: center; margin: 20px 0; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🎉 Happy Birthday, {name}! 🎉</h1>
                {f"<p>Wishing you an amazing {age}th birthday!</p>" if age else ""}
            </div>
            
            <div class="content">
                <p>Dear {name},</p>
                
                <p>On this special day, we want to celebrate YOU! 🎂</p>
                
                <p>We hope your birthday is filled with happiness, laughter, and all your favorite things. 
                Thank you for being such an amazing part of our team!</p>
                
                <div class="flyer">
                    <p><strong>Your personalized birthday flyer is attached!</strong></p>
                </div>
                
                <p>Have a wonderful day and an even better year ahead!</p>
                
                <p>With warmest wishes,<br>
                The Drawtab Team</p>
            </div>
            
            <div class="footer">
                <p>This message was automatically generated by Drawtab</p>
            </div>
        </div>
    </body>
    </html>
    """

    text_body = f"""
    Happy Birthday, {name}!
    
    Dear {name},
    
    On this special day, we want to celebrate YOU!
    
    We hope your birthday is filled with happiness, laughter, and all your favorite things.
    Thank you for being such an amazing part of our team!
    
    Your personalized birthday flyer is attached!
    
    Have a wonderful day and an even better year ahead!
    
    With warmest wishes,
    The Drawtab Team
    
    ---
    This message was automatically generated by Drawtab
    """

    return {
        'subject': subject,
        'htmlBody': html_body,
        'textBody': text_body
    }


def generate_anniversary_email_template(name: str, years: int = None, anniversary_type: str = 'work') -> Dict[str, str]:
    """
    Generate anniversary email template
    """
    if anniversary_type == 'work':
        subject = f"🎉 Congratulations on your work anniversary, {name}!"
        celebration_text = f"work anniversary{f' - {years} years' if years else ''}!"
    else:
        subject = f"💕 Happy Anniversary, {name}!"
        celebration_text = f"anniversary{f' - {years} years' if years else ''}!"

    html_body = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>Happy Anniversary!</title>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); color: white; padding: 30px; text-align: center; border-radius: 10px; }}
            .content {{ padding: 30px 20px; background: #f9f9f9; border-radius: 10px; margin: 20px 0; }}
            .footer {{ text-align: center; color: #666; padding: 20px; }}
            .flyer {{ text-align: center; margin: 20px 0; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🎉 Happy {celebration_text.title()} 🎉</h1>
                <p>Celebrating {name}</p>
            </div>
            
            <div class="content">
                <p>Dear {name},</p>
                
                <p>Today marks a special milestone - your {celebration_text}</p>
                
                <p>{"We're grateful for your dedication and all the amazing work you've done over the years." if anniversary_type == 'work' else "We're celebrating this beautiful milestone with you!"}</p>
                
                <div class="flyer">
                    <p><strong>Your personalized anniversary flyer is attached!</strong></p>
                </div>
                
                <p>{"Here's to many more successful years ahead!" if anniversary_type == 'work' else "Here's to many more wonderful years together!"}</p>
                
                <p>With appreciation,<br>
                The Drawtab Team</p>
            </div>
            
            <div class="footer">
                <p>This message was automatically generated by Drawtab</p>
            </div>
        </div>
    </body>
    </html>
    """

    text_body = f"""
    Happy {celebration_text.title()}
    
    Dear {name},
    
    Today marks a special milestone - your {celebration_text}
    
    {"We're grateful for your dedication and all the amazing work you've done over the years." if anniversary_type == 'work' else "We're celebrating this beautiful milestone with you!"}
    
    Your personalized anniversary flyer is attached!
    
    {"Here's to many more successful years ahead!" if anniversary_type == 'work' else "Here's to many more wonderful years together!"}
    
    With appreciation,
    The Drawtab Team
    
    ---
    This message was automatically generated by Drawtab
    """

    return {
        'subject': subject,
        'htmlBody': html_body,
        'textBody': text_body
    }


# Required for Appwrite function runtime
if __name__ == '__main__':
    pass
