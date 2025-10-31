def get_guidance_for_crime(crime_type):
    responses = {
        "phishing": (
            "⚠️ This appears to be a phishing attempt. Do not click any suspicious links "
            "or share your personal/banking details. Report it immediately at "
            "https://www.cybercrime.gov.in/ or to your email provider."
        ),

        "cyberstalking": (
            "💬 It looks like you're being cyberstalked. Block the person, document their activities, "
            "and avoid engaging. File a report with your local cybercrime police or online portal."
        ),

        "ransomware": (
            "💻 Your system might be affected by ransomware. Disconnect it from all networks, "
            "avoid paying ransom, and contact a professional or cybercrime authorities."
        ),

        "identity theft": (
            "🆔 This seems like an identity theft case. Immediately change passwords, inform your bank, "
            "and file a report at https://www.cybercrime.gov.in/."
        ),

        "online harassment": (
            "💢 You’re facing online harassment. Block and report the user, take screenshots as evidence, "
            "and reach out to authorities or trusted contacts for support."
        ),

        "financial fraud": (
            "💰 It seems like a financial scam. Contact your bank immediately to freeze transactions "
            "and file a report on the cybercrime portal."
        ),

        "social media hacking": (
            "🔐 Your social media account might have been hacked. Change passwords right away, "
            "enable two-factor authentication, and report the account to the platform’s support team."
        ),

        "fake job offer": (
            "📩 This might be a fake job offer scam. Avoid sharing personal or financial details "
            "and verify the company through official websites or LinkedIn before proceeding."
        ),

        "loan scam": (
            "🏦 It seems like a loan scam. Do not transfer any money or share OTPs. "
            "Report it to your bank and the cybercrime portal immediately."
        ),

        "fake shopping website": (
            "🛒 You might have encountered a fake shopping site. Avoid further transactions "
            "and report the website to cyber authorities."
        ),

        "romance scam": (
            "❤️ This seems like a romance scam. Be cautious of anyone asking for money or personal information online. "
            "Block and report them immediately."
        ),

        "data breach": (
            "📁 A data breach may have exposed your information. Change all passwords, enable 2FA, "
            "and monitor your financial accounts for suspicious activity."
        ),

        "email spoofing": (
            "📧 It appears to be email spoofing. Do not respond or click links. "
            "Check the sender’s real email domain and report it as spam."
        ),

        "malware attack": (
            "🐞 Your system may be infected with malware. Run a trusted antivirus scan, "
            "disconnect from the internet, and seek IT support."
        ),

        "SIM swapping": (
            "📱 This looks like a SIM swapping case. Contact your mobile service provider immediately "
            "to block your SIM and secure your linked accounts."
        ),

        "cryptocurrency fraud": (
            "₿ This seems like a crypto-related scam. Never share your wallet credentials or private keys. "
            "Report the fraud at https://www.cybercrime.gov.in/."
        ),

        "unknown": (
            "🤔 I couldn't clearly identify the cybercrime type. Please describe your situation in more detail, "
            "and I’ll try to guide you further."
        ),
    }

    return responses.get(crime_type.lower(), responses["unknown"])
