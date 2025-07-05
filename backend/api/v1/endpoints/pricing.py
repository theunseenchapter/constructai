# Pricing API endpoints for dynamic material price management
from typing import Dict, List, Any, Optional
from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from pydantic import BaseModel
from datetime import datetime
import logging

# Import pricing system
from core.pricing import (
    DynamicPricingSystem, 
    PriceUpdate, 
    PriceResponse,
    MATERIAL_CODE_MAPPING
)
from core.database import get_sync_db

router = APIRouter()
logger = logging.getLogger(__name__)

class PriceUpdateRequest(BaseModel):
    material_code: str
    new_price: float
    source: str = "manual"
    notes: Optional[str] = None

class BulkPriceUpdateRequest(BaseModel):
    updates: List[PriceUpdateRequest]

@router.get("/current-prices", response_model=Dict[str, Any])
async def get_current_prices():
    """Get all current material prices with market trends"""
    try:
        db = get_sync_db()
        if not db:
            raise HTTPException(status_code=503, detail="Database not available")
        
        pricing_system = DynamicPricingSystem(db)
        prices = pricing_system.get_current_prices()
        
        return {
            "success": True,
            "prices": prices,
            "total_materials": len(prices),
            "last_updated": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error fetching current prices: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching prices: {str(e)}")

@router.get("/market-summary")
async def get_market_summary():
    """Get market summary with trends and statistics"""
    try:
        db = get_sync_db()
        if not db:
            raise HTTPException(status_code=503, detail="Database not available")
        
        pricing_system = DynamicPricingSystem(db)
        summary = pricing_system.get_market_summary()
        
        return {"success": True, "data": summary}
    except Exception as e:
        logger.error(f"Error fetching market summary: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching market summary: {str(e)}")

@router.get("/price-history/{material_code}")
async def get_price_history(material_code: str, days: int = 30):
    """Get price history for a specific material"""
    try:
        db = get_sync_db()
        if not db:
            raise HTTPException(status_code=503, detail="Database not available")
        
        pricing_system = DynamicPricingSystem(db)
        history = pricing_system.get_price_history(material_code, days)
        
        if not history:
            raise HTTPException(status_code=404, detail="Material not found or no price history")
        
        return {
            "success": True,
            "material_code": material_code,
            "days": days,
            "history": history
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching price history: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching price history: {str(e)}")

@router.post("/update-price")
async def update_material_price(price_update: PriceUpdateRequest):
    """Update price for a specific material"""
    try:
        db = get_sync_db()
        if not db:
            raise HTTPException(status_code=503, detail="Database not available")
        
        pricing_system = DynamicPricingSystem(db)
        result = await pricing_system.update_material_price(
            price_update.material_code,
            price_update.new_price,
            price_update.source
        )
        
        if not result["updated"]:
            raise HTTPException(status_code=400, detail=result.get("error", "Failed to update price"))
        
        return {"success": True, "data": result}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating material price: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error updating price: {str(e)}")

@router.post("/bulk-update-prices")
async def bulk_update_prices(bulk_update: BulkPriceUpdateRequest):
    """Update multiple material prices in bulk"""
    try:
        db = get_sync_db()
        if not db:
            raise HTTPException(status_code=503, detail="Database not available")
        
        pricing_system = DynamicPricingSystem(db)
        results = []
        success_count = 0
        
        for update in bulk_update.updates:
            try:
                result = await pricing_system.update_material_price(
                    update.material_code,
                    update.new_price,
                    update.source
                )
                results.append(result)
                if result["updated"]:
                    success_count += 1
            except Exception as e:
                results.append({
                    "updated": False,
                    "material_code": update.material_code,
                    "error": str(e)
                })
        
        return {
            "success": True,
            "total_updates": len(bulk_update.updates),
            "successful_updates": success_count,
            "results": results
        }
    except Exception as e:
        logger.error(f"Error in bulk price update: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error in bulk update: {str(e)}")

@router.post("/refresh-live-prices")
async def refresh_live_prices(background_tasks: BackgroundTasks):
    """Refresh all prices from live market sources"""
    try:
        db = get_sync_db()
        if not db:
            raise HTTPException(status_code=503, detail="Database not available")
        
        pricing_system = DynamicPricingSystem(db)
        
        # Run price update in background
        async def update_prices():
            try:
                result = await pricing_system.update_all_prices()
                logger.info(f"Live price update completed: {result}")
            except Exception as e:
                logger.error(f"Background price update failed: {str(e)}")
        
        background_tasks.add_task(update_prices)
        
        return {
            "success": True,
            "message": "Live price update initiated in background",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error initiating live price refresh: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error initiating price refresh: {str(e)}")

@router.get("/material-codes")
async def get_material_codes():
    """Get list of all available material codes and mappings"""
    try:
        db = get_sync_db()
        if not db:
            raise HTTPException(status_code=503, detail="Database not available")
        
        pricing_system = DynamicPricingSystem(db)
        current_prices = pricing_system.get_current_prices()
        
        material_info = {}
        for code, data in current_prices.items():
            material_info[code] = {
                "name": data["material_name"],
                "unit": data["unit"],
                "current_price": data["rate"],
                "market_trend": data["market_trend"]
            }
        
        return {
            "success": True,
            "materials": material_info,
            "legacy_mapping": MATERIAL_CODE_MAPPING,
            "total_materials": len(material_info)
        }
    except Exception as e:
        logger.error(f"Error fetching material codes: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching material codes: {str(e)}")

@router.get("/price-comparison/{material_code}")
async def get_price_comparison(material_code: str, days: int = 7):
    """Get price comparison and trend analysis for a material"""
    try:
        db = get_sync_db()
        if not db:
            raise HTTPException(status_code=503, detail="Database not available")
        
        pricing_system = DynamicPricingSystem(db)
        history = pricing_system.get_price_history(material_code, days)
        
        if not history:
            raise HTTPException(status_code=404, detail="Material not found")
        
        # Calculate statistics
        prices = [entry["price"] for entry in history]
        if prices:
            min_price = min(prices)
            max_price = max(prices)
            avg_price = sum(prices) / len(prices)
            current_price = prices[-1] if prices else 0
            
            price_range = max_price - min_price
            volatility = (price_range / avg_price) * 100 if avg_price > 0 else 0
            
            return {
                "success": True,
                "material_code": material_code,
                "analysis_period_days": days,
                "statistics": {
                    "current_price": current_price,
                    "min_price": min_price,
                    "max_price": max_price,
                    "average_price": round(avg_price, 2),
                    "price_range": round(price_range, 2),
                    "volatility_percentage": round(volatility, 2)
                },
                "price_history": history
            }
        else:
            return {
                "success": False,
                "error": "No price data available for analysis"
            }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in price comparison: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error in price comparison: {str(e)}")
