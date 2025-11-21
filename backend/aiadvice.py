from openai import OpenAI

# Hardcoded key because you told me to keep it visible
client = OpenAI(api_key="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")

def debug(msg):
    print(f"[DEBUG] {msg}")

def format_portfolio(user_data):
    debug(f"Formatting portfolio: {user_data}")

    balance = user_data.get("balance", 0)
    positions = user_data.get("positions", [])

    debug(f"Balance: {balance}")
    debug(f"Positions count: {len(positions)}")

    if not positions:
        result = f"Balance: ${balance:.2f}\nNo stocks owned yet! You're just hoarding cash like a dragon 🐉💰"
        debug(f"Formatted summary:\n{result}")
        return result

    text = [f"Balance: ${balance:.2f}", "\nStock Holdings:\n"]
    total_value = balance

    for p in positions:
        debug(f"Processing position: {p}")

        symbol = p.get("symbol", "UNKNOWN")
        shares = p.get("shares", 0)
        price = p.get("price", 0)
        value = p.get("totalValue", 0)
        profit = p.get("profit", 0)
        percent = p.get("profitPercent", 0)

        total_value += value
        emoji = "📈" if profit >= 0 else "📉"

        line = (
            f"- {symbol}: {shares} shares @ ${price:.2f} | "
            f"Value: ${value:.2f} | P/L: ${profit:.2f} ({percent:.1f}%) {emoji}"
        )
        debug(f"Line added: {line}")
        text.append(line)

    summary = "\n".join(text) + f"\n\nTotal Portfolio Value: ${total_value:.2f}"
    debug(f"Final portfolio summary:\n{summary}")

    return summary

def get_funny_financial_advice(user_data):
    try:
        debug("=== get_funny_financial_advice START ===")
        debug(f"User data received: {user_data}")

        summary = format_portfolio(user_data)

        prompt = f"Here is my portfolio:\n{summary}\nGive advice:"
        debug(f"Constructed prompt:\n{prompt}")

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are a playful, funny mommy-style financial advisor. "
                               "Keep advice short (2–3 sentences max) and use emojis."
                },
                {"role": "user", "content": prompt}
            ],
            max_tokens=120,
            temperature=0.9
        )

        debug("Raw OpenAI response received:")
        debug(response)

        final = response.choices[0].message.content.strip()
        debug(f"Final extracted advice: {final}")

        debug("=== get_funny_financial_advice END ===")

        return final

    except Exception as e:
        debug(f"ERROR in get_funny_financial_advice: {e}")
        return "💸 Mommy can't read the stock charts right now. Try again later, sweetie!"
