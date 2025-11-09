from openai import OpenAI
import os

# Initialize OpenAI client
client = OpenAI(api_key="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")

def format_portfolio(user_data):
    """Format user portfolio data for the prompt"""
    positions = user_data.get('positions', [])
    balance = user_data.get('balance', 0)
    
    print(f"DEBUG - Balance: {balance}")
    print(f"DEBUG - Positions: {positions}")
    
    if not positions:
        return f"Balance: ${balance:.2f}\nNo stocks owned yet! Just sitting on cash like a cozy cushion! 💰"
    
    portfolio_text = f"Balance: ${balance:.2f}\n\nStock Holdings:\n"
    total_portfolio_value = balance
    
    for position in positions:
        symbol = position.get('symbol', 'UNKNOWN')
        shares = position.get('shares', 0)
        price = position.get('price', 0)
        total_value = position.get('totalValue', 0)
        profit = position.get('profit', 0)
        profit_percent = position.get('profitPercent', 0)
        
        total_portfolio_value += total_value
        
        profit_emoji = "📈" if profit >= 0 else "📉"
        portfolio_text += f"- {symbol}: {shares} shares @ ${price:.2f} | Value: ${total_value:.2f} | P/L: ${profit:.2f} ({profit_percent:.1f}%) {profit_emoji}\n"
    
    portfolio_text += f"\nTotal Portfolio Value: ${total_portfolio_value:.2f}"
    
    return portfolio_text

def get_funny_financial_advice(user_data):
    """
    Get funny, playful financial advice from GPT based on user's portfolio
    
    Args:
        user_data (dict): User data with 'balance' and 'positions'
    
    Returns:
        str: Funny financial advice
    """
    try:
        print("DEBUG - Starting get_funny_financial_advice")
        print(f"DEBUG - User data: {user_data}")
        
        portfolio_summary = format_portfolio(user_data)
        print(f"DEBUG - Portfolio summary: {portfolio_summary}")
        
        prompt = f"""You are a sassy, funny financial advisor in a playful "mommy simulator" game. 
Give SHORT, humorous financial advice (2-3 sentences max) based on this player's portfolio. 
Be playful, use emojis, and make it entertaining while still being somewhat helpful.
Don't be too harsh if they're losing money - keep it light and supportive!

Portfolio:
{portfolio_summary}

Give your advice:"""

        print("DEBUG - Calling OpenAI API...")
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a funny, sassy financial advisor in a cute game. Keep responses brief and entertaining."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150,
            temperature=0.9
        )
        
        print("DEBUG - Got response from OpenAI")
        advice = response.choices[0].message.content.strip()
        print(f"DEBUG - Advice: {advice}")
        return advice
        
    except Exception as e:
        print(f"ERROR getting AI advice: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return "💸 Oops! My crystal ball is cloudy right now. Try diversifying your portfolio... or just buy more cute accessories! 🛍️"