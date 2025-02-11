from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
import time
from datetime import datetime
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

def setup_chrome_options():
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    return chrome_options

@app.get('/health')
def health_check():
    return {'status': 'healthy'}

@app.post('/screenshot')
async def take_screenshot(symbol: str = 'EURUSD', timeframe: str = '1h'):
    try:
        logger.info(f"📸 Taking screenshot for {symbol} {timeframe}")
        
        # TradingView URL
        url = f"https://www.tradingview.com/chart/?symbol={symbol}&interval={timeframe}"
        
        # Setup Chrome
        chrome_options = setup_chrome_options()
        driver = webdriver.Chrome(options=chrome_options)
        
        try:
            # Get page
            driver.get(url)
            time.sleep(5)  # Wait for chart to load
            
            # Zoom in op de chart
            driver.execute_script("""
                const chart = document.querySelector('div[class*="chart-container"]');
                if (chart) {
                    chart.style.transform = 'scale(1.5)';  // 50% inzoomen
                    chart.style.transformOrigin = 'center center';
                }
            """)
            
            time.sleep(2)  # Wait for zoom effect
            
            # Take screenshot
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"/tmp/screenshots/{symbol}_{timeframe}_{timestamp}.png"
            
            # Ensure directory exists
            os.makedirs('/tmp/screenshots', exist_ok=True)
            
            driver.save_screenshot(filename)
            logger.info(f"✅ Screenshot saved: {filename}")
            
            return FileResponse(filename, media_type='image/png')
            
        finally:
            driver.quit()
            
    except Exception as e:
        logger.error(f"❌ Screenshot error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
