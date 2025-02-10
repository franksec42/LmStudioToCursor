# LMStudio-Cursor Integration

This project allows you to integrate LMStudio's open-source models with Cursor, providing a seamless experience similar to using GPT-4.

## Prerequisites

- Python 3.10
- LMStudio
- Cursor

## Installation

To install the required dependencies, run the following command:

```bash
pip install -r requirements.txt
```

This will install all required dependencies:
- Flask 3.0.3
- Flask-Cors 4.0.1
- OpenAI 1.42.0
- HTTPX 0.27.0
- Anyio 4.4.0
- Typing Extensions 4.12.2

## Setup

1. Start the LMStudio server:
   - Open LMStudio
   - Select your desired model
   - Start the local server

2. Configure the Python script:
   - Open `v1.py`
   - Update the `base_url` in the `OpenAI` client initialization to match LMStudio's server address (usually `http://localhost:1234/v1`)
   - Update the `model` variable in the `chat_endpoint` function to match your chosen LMStudio model name

3. Run the Python script:
   ```
   python v1.py
   ```

4. Set up port forwarding:
   - Forward port 5000 to make it accessible

5. Configure Cursor:
   - Open Cursor settings
   - In the GPT-4 configuration:
     - Set the API Key to any value (e.g., "lm-studio")
     - Set the API URL to your forwarded port address (e.g., `https://your-forwarded-address-5000.com`)

6. Select GPT-4 in Cursor:
   - Cursor will now use your LMStudio model instead of the official GPT-4

## Reverting to OpenAI GPT-4

To switch back to the official OpenAI GPT-4:
1. Open Cursor settings
2. Disable or remove the custom OpenAI API Key
3. Cursor will automatically revert to using the built-in GPT-4 integration

## Note

This setup allows you to leverage open-source models through LMStudio while maintaining the Cursor interface. Always ensure you comply with the terms of service and licensing agreements of all involved software.

## Contributing

We welcome contributions to improve this integration! Here's how you can help:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/improvement`)
3. Make your changes
4. Commit your changes (`git commit -am 'Add new feature'`)
5. Push to the branch (`git push origin feature/improvement`)
6. Create a Pull Request

## Social Media and Contact

- GitHub: [LmStudioToCursor](https://github.com/olweraltuve/LmStudioToCursor)
- LinkedIn: [Oliver Altuve](https://www.linkedin.com/in/olwer-altuve-santaromita-97824518a/)
- Email: olwerjose33@hotmail.com

For questions or support, feel free to:
- Open an issue on GitHub
- Send an email
- Connect with me on LinkedIn