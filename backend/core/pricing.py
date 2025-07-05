# Dynamic Pricing System for Construction Materials
# Real-time market price integration and management

from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from pydantic import BaseModel
import requests
import json
import asyncio
import logging
from decimal import Decimal

# Optional SQLAlchemy imports
try:
    from sqlalchemy import Column, String, Float, DateTime, Boolean, Text, Integer
    from sqlalchemy.ext.declarative import declarative_base
    from sqlalchemy.orm import Session
    SQLALCHEMY_AVAILABLE = True
    Base = declarative_base()
except ImportError:
    SQLALCHEMY_AVAILABLE = False
    Column = None
    String = None
    Float = None
    DateTime = None
    Boolean = None
    Text = None
    Integer = None
    declarative_base = None
    Session = None
    Base = None

if SQLALCHEMY_AVAILABLE:
    class MaterialPrice(Base):
        """Database model for storing material prices"""
        __tablename__ = "material_prices"
        
        id = Column(Integer, primary_key=True, index=True)
        material_code = Column(String(50), unique=True, index=True)
        material_name = Column(String(200), nullable=False)
        current_price = Column(Float, nullable=False)
        unit = Column(String(20), nullable=False)
        weight_kg = Column(Float, default=0)
        last_updated = Column(DateTime, default=datetime.utcnow)
        source = Column(String(100), default="manual")  # manual, api, scraping
        is_active = Column(Boolean, default=True)
        price_history = Column(Text)  # JSON string of historical prices
        fluctuation_percentage = Column(Float, default=0.0)  # Daily change %
        market_trend = Column(String(20), default="stable")  # rising, falling, stable
else:
    class MaterialPrice:
        """Dummy model when SQLAlchemy is not available"""
        pass

class PriceUpdate(BaseModel):
    """Model for price update requests"""
    material_code: str
    new_price: float
    source: str = "manual"
    notes: Optional[str] = None

class PriceResponse(BaseModel):
    """Response model for price data"""
    material_code: str
    material_name: str
    current_price: float
    unit: str
    last_updated: datetime
    fluctuation_percentage: float
    market_trend: str
    price_history: List[Dict[str, Any]]

class DynamicPricingSystem:
    """Dynamic pricing system with real-time market integration"""
    
    def __init__(self, db_session):
        self.db = db_session
        self.logger = logging.getLogger(__name__)
        
        # Market data sources (these would be real APIs in production)
        self.price_apis = {
            "commodity_api": "https://api.commoditiesapi.com/v1/latest",
            "metal_prices": "https://metals-api.com/api/latest",
            "construction_index": "https://api.constructionindex.com/v1/prices"
        }
        
        # Initialize default materials if not exists
        if SQLALCHEMY_AVAILABLE:
            self._initialize_default_materials()
    
    def _initialize_default_materials(self):
        """Initialize default materials with current market rates"""
        if not SQLALCHEMY_AVAILABLE:
            return
            
        default_materials = [
            {
                "material_code": "cement_opc_53",
                "material_name": "OPC 53 Grade Cement",
                "current_price": 420.0,  # Updated base price
                "unit": "bag",
                "weight_kg": 50,
                "source": "market_data"
            },
            {
                "material_code": "steel_tmt_8mm",
                "material_name": "TMT Steel Bar 8mm",
                "current_price": 68000.0,  # Current steel prices
                "unit": "ton",
                "weight_kg": 1000,
                "source": "market_data"
            },
            {
                "material_code": "steel_tmt_12mm",
                "material_name": "TMT Steel Bar 12mm",
                "current_price": 67500.0,
                "unit": "ton",
                "weight_kg": 1000,
                "source": "market_data"
            },
            {
                "material_code": "bricks_red_clay",
                "material_name": "Red Clay Bricks",
                "current_price": 9.5,  # Per piece, regional variation
                "unit": "piece",
                "weight_kg": 3,
                "source": "market_data"
            },
            {
                "material_code": "sand_river",
                "material_name": "River Sand",
                "current_price": 1800.0,  # Price volatility due to regulations
                "unit": "cft",
                "weight_kg": 35,
                "source": "market_data"
            },
            {
                "material_code": "aggregate_20mm",
                "material_name": "Coarse Aggregate 20mm",
                "current_price": 2200.0,
                "unit": "cft",
                "weight_kg": 40,
                "source": "market_data"
            },
            {
                "material_code": "concrete_m25_rmc",
                "material_name": "Ready Mix Concrete M25",
                "current_price": 6200.0,  # RMC prices with fuel costs
                "unit": "cum",
                "weight_kg": 2400,
                "source": "market_data"
            },
            {
                "material_code": "tiles_vitrified_600x600",
                "material_name": "Vitrified Tiles 600x600mm",
                "current_price": 850.0,
                "unit": "sqm",
                "weight_kg": 20,
                "source": "market_data"
            },
            {
                "material_code": "paint_exterior_premium",
                "material_name": "Premium Exterior Paint",
                "current_price": 140.0,
                "unit": "sqm",
                "weight_kg": 2,
                "source": "market_data"
            },
            {
                "material_code": "door_teak_premium",
                "material_name": "Teak Wood Door Premium",
                "current_price": 18000.0,  # Wood prices fluctuate significantly
                "unit": "piece",
                "weight_kg": 50,
                "source": "market_data"
            },
            {
                "material_code": "window_upvc_standard",
                "material_name": "UPVC Window Standard",
                "current_price": 5500.0,
                "unit": "piece",
                "weight_kg": 30,
                "source": "market_data"
            }
        ]
        
        for material_data in default_materials:
            if not SQLALCHEMY_AVAILABLE:
                continue
                
            existing = self.db.query(MaterialPrice).filter(
                MaterialPrice.material_code == material_data["material_code"]
            ).first()
            
            if not existing:
                material = MaterialPrice(**material_data)
                material.price_history = json.dumps([{
                    "date": datetime.now().isoformat(),
                    "price": material_data["current_price"],
                    "source": "initialization"
                }])
                self.db.add(material)
        
        if SQLALCHEMY_AVAILABLE:
            self.db.commit()
    
    async def fetch_live_prices(self) -> Dict[str, float]:
        """Fetch live prices from market APIs"""
        live_prices = {}
        
        try:
            # Simulate API calls for different material categories
            # In production, these would be real API calls
            
            # Steel prices (affected by global commodity markets)
            steel_fluctuation = self._calculate_market_fluctuation("steel")
            base_steel_price = 67000
            live_prices["steel_tmt_8mm"] = base_steel_price * (1 + steel_fluctuation/100)
            live_prices["steel_tmt_12mm"] = base_steel_price * 0.99 * (1 + steel_fluctuation/100)
            
            # Cement prices (affected by fuel costs and regional demand)
            cement_fluctuation = self._calculate_market_fluctuation("cement")
            live_prices["cement_opc_53"] = 420 * (1 + cement_fluctuation/100)
            
            # Sand prices (highly regulated, volatile)
            sand_fluctuation = self._calculate_market_fluctuation("sand", volatility=0.15)
            live_prices["sand_river"] = 1800 * (1 + sand_fluctuation/100)
            
            # Ready mix concrete (fuel costs + material costs)
            rmc_fluctuation = (steel_fluctuation + cement_fluctuation) / 2
            live_prices["concrete_m25_rmc"] = 6200 * (1 + rmc_fluctuation/100)
            
            # Wood prices (seasonal and availability based)
            wood_fluctuation = self._calculate_market_fluctuation("wood", volatility=0.12)
            live_prices["door_teak_premium"] = 18000 * (1 + wood_fluctuation/100)
            
            # Tile prices (relatively stable but affected by energy costs)
            tile_fluctuation = self._calculate_market_fluctuation("tiles", volatility=0.05)
            live_prices["tiles_vitrified_600x600"] = 850 * (1 + tile_fluctuation/100)
            
            self.logger.info(f"Fetched live prices for {len(live_prices)} materials")
            
        except Exception as e:
            self.logger.error(f"Error fetching live prices: {str(e)}")
            
        return live_prices
    
    def _calculate_market_fluctuation(self, material_category: str, volatility: float = 0.08) -> float:
        """Calculate realistic market fluctuation based on current trends"""
        import random
        
        # Simulate realistic market conditions
        base_trends = {
            "steel": 0.02,    # Generally rising due to infrastructure demand
            "cement": 0.015,  # Moderate increase
            "sand": -0.01,    # Slight decrease due to regulations
            "wood": 0.035,    # Rising due to sustainability concerns
            "tiles": 0.008,   # Stable with slight increase
            "default": 0.01
        }
        
        trend = base_trends.get(material_category, base_trends["default"])
        
        # Add random daily fluctuation
        daily_change = random.uniform(-volatility, volatility)
        
        # Combine trend with daily volatility
        total_fluctuation = trend + daily_change
        
        return round(total_fluctuation * 100, 2)  # Return as percentage
    
    async def update_all_prices(self) -> Dict[str, Any]:
        """Update all material prices from live sources"""
        try:
            live_prices = await self.fetch_live_prices()
            updated_count = 0
            price_changes = []
            
            for material_code, new_price in live_prices.items():
                result = await self.update_material_price(material_code, new_price, "live_api")
                if result["updated"]:
                    updated_count += 1
                    price_changes.append({
                        "material": material_code,
                        "old_price": result["old_price"],
                        "new_price": new_price,
                        "change_percent": result["change_percent"]
                    })
            
            return {
                "success": True,
                "updated_count": updated_count,
                "total_materials": len(live_prices),
                "price_changes": price_changes,
                "last_updated": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Error updating prices: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def get_current_prices(self) -> Dict[str, Dict[str, Any]]:
        """Get all current material prices"""
        if not SQLALCHEMY_AVAILABLE:
            return self._get_fallback_prices()
            
        materials = self.db.query(MaterialPrice).filter(MaterialPrice.is_active == True).all()
        
        prices = {}
        for material in materials:
            prices[material.material_code] = {
                "rate": material.current_price,
                "unit": material.unit,
                "weight_kg": material.weight_kg,
                "last_updated": material.last_updated.isoformat(),
                "fluctuation_percentage": material.fluctuation_percentage,
                "market_trend": material.market_trend,
                "material_name": material.material_name
            }
        
        return prices
    
    def _get_fallback_prices(self) -> Dict[str, Dict[str, Any]]:
        """Fallback prices when database is not available"""
        return {
            "cement_opc_53": {
                "rate": 420.0,
                "unit": "bag",
                "weight_kg": 50,
                "last_updated": datetime.now().isoformat(),
                "fluctuation_percentage": 0.0,
                "market_trend": "stable",
                "material_name": "OPC 53 Grade Cement"
            },
            "steel_tmt_8mm": {
                "rate": 68000.0,
                "unit": "ton",
                "weight_kg": 1000,
                "last_updated": datetime.now().isoformat(),
                "fluctuation_percentage": 0.0,
                "market_trend": "stable",
                "material_name": "TMT Steel Bar 8mm"
            },
            "sand_river": {
                "rate": 1800.0,
                "unit": "ton",
                "weight_kg": 1000,
                "last_updated": datetime.now().isoformat(),
                "fluctuation_percentage": 0.0,
                "market_trend": "stable",
                "material_name": "River Sand"
            },
            "concrete_m25_rmc": {
                "rate": 6200.0,
                "unit": "cum",
                "weight_kg": 2400,
                "last_updated": datetime.now().isoformat(),
                "fluctuation_percentage": 0.0,
                "market_trend": "stable",
                "material_name": "Ready Mix Concrete M25"
            }
        }

    async def update_material_price(self, material_code: str, new_price: float, source: str = "manual") -> Dict[str, Any]:
        """Update price for a specific material"""
        if not SQLALCHEMY_AVAILABLE:
            return {"updated": False, "error": "Database not available"}
            
        try:
            material = self.db.query(MaterialPrice).filter(
                MaterialPrice.material_code == material_code
            ).first()
            
            if not material:
                return {"updated": False, "error": "Material not found"}
            
            old_price = material.current_price
            change_percent = ((new_price - old_price) / old_price) * 100 if old_price > 0 else 0
            
            # Update price history
            price_history = json.loads(material.price_history or "[]")
            price_history.append({
                "date": datetime.now().isoformat(),
                "price": new_price,
                "source": source,
                "change_percent": round(change_percent, 2)
            })
            
            # Keep only last 30 entries
            if len(price_history) > 30:
                price_history = price_history[-30:]
            
            # Determine market trend
            if change_percent > 2:
                trend = "rising"
            elif change_percent < -2:
                trend = "falling"
            else:
                trend = "stable"
            
            # Update material
            material.current_price = new_price
            material.last_updated = datetime.now()
            material.source = source
            material.price_history = json.dumps(price_history)
            material.fluctuation_percentage = round(change_percent, 2)
            material.market_trend = trend
            
            self.db.commit()
            
            return {
                "updated": True,
                "material_code": material_code,
                "old_price": old_price,
                "new_price": new_price,
                "change_percent": round(change_percent, 2),
                "trend": trend
            }
            
        except Exception as e:
            self.logger.error(f"Error updating material price: {str(e)}")
            return {"updated": False, "error": str(e)}

    def get_price_history(self, material_code: str, days: int = 30) -> List[Dict[str, Any]]:
        """Get price history for a material"""
        if not SQLALCHEMY_AVAILABLE:
            return []
            
        material = self.db.query(MaterialPrice).filter(
            MaterialPrice.material_code == material_code
        ).first()
        
        if not material:
            return []
        
        price_history = json.loads(material.price_history or "[]")
        
        # Filter by date range if needed
        cutoff_date = datetime.now() - timedelta(days=days)
        filtered_history = [
            entry for entry in price_history
            if datetime.fromisoformat(entry["date"]) >= cutoff_date
        ]
        
        return filtered_history

    def get_market_summary(self) -> Dict[str, Any]:
        """Get market summary with trends and statistics"""
        if not SQLALCHEMY_AVAILABLE:
            return {
                "total_materials": 4,
                "rising_trend": 0,
                "falling_trend": 0,
                "stable_trend": 4,
                "average_fluctuation": 0.0,
                "most_volatile": "cement_opc_53",
                "most_stable": "steel_tmt_8mm",
                "last_updated": datetime.now().isoformat()
            }
            
        materials = self.db.query(MaterialPrice).filter(MaterialPrice.is_active == True).all()
        
        if not materials:
            return {"error": "No materials found"}
        
        rising_count = sum(1 for m in materials if m.market_trend == "rising")
        falling_count = sum(1 for m in materials if m.market_trend == "falling")
        stable_count = sum(1 for m in materials if m.market_trend == "stable")
        
        avg_fluctuation = sum(m.fluctuation_percentage for m in materials) / len(materials)
        
        most_volatile = max(materials, key=lambda m: abs(m.fluctuation_percentage))
        
        return {
            "total_materials": len(materials),
            "market_trends": {
                "rising": rising_count,
                "falling": falling_count,
                "stable": stable_count
            },
            "average_fluctuation": round(avg_fluctuation, 2),
            "most_volatile_material": {
                "code": most_volatile.material_code,
                "name": most_volatile.material_name,
                "fluctuation": most_volatile.fluctuation_percentage
            },
            "last_update": max(m.last_updated for m in materials).isoformat()
        }

# Mapping from old static codes to new dynamic codes
MATERIAL_CODE_MAPPING = {
    "cement": "cement_opc_53",
    "steel": "steel_tmt_8mm",
    "bricks": "bricks_red_clay",
    "sand": "sand_river",
    "aggregate": "aggregate_20mm",
    "concrete_m25": "concrete_m25_rmc",
    "tiles": "tiles_vitrified_600x600",
    "paint": "paint_exterior_premium",
    "door_premium": "door_teak_premium",
    "window_standard": "window_upvc_standard",
    # Add more mappings as needed
}

def get_dynamic_material_rates(pricing_system: DynamicPricingSystem) -> Dict[str, Dict[str, Any]]:
    """Get current dynamic material rates compatible with existing BOQ system"""
    dynamic_prices = pricing_system.get_current_prices()
    
    # Convert to old format for backward compatibility
    material_rates = {}
    
    for old_code, new_code in MATERIAL_CODE_MAPPING.items():
        if new_code in dynamic_prices:
            price_data = dynamic_prices[new_code]
            material_rates[old_code] = {
                "rate": price_data["rate"],
                "unit": price_data["unit"],
                "weight_kg": price_data["weight_kg"],
                "last_updated": price_data["last_updated"],
                "market_trend": price_data["market_trend"],
                "fluctuation": price_data["fluctuation_percentage"]
            }
    
    # Add static rates for items not yet in dynamic system
    static_fallbacks = {
        "rcc_slab": {"rate": 6800, "unit": "sqm", "weight_kg": 375},
        "brick_wall": {"rate": 480, "unit": "sqm", "weight_kg": 400},
        "plaster": {"rate": 195, "unit": "sqm", "weight_kg": 25},
        "electrical": {"rate": 16500, "unit": "room", "weight_kg": 50},
        "plumbing": {"rate": 13500, "unit": "room", "weight_kg": 80},
        "door_standard": {"rate": 9200, "unit": "piece", "weight_kg": 45},
        "window_premium": {"rate": 8800, "unit": "piece", "weight_kg": 30},
        "door_frame": {"rate": 2800, "unit": "piece", "weight_kg": 15},
        "window_frame": {"rate": 2000, "unit": "piece", "weight_kg": 10}
    }
    
    for code, data in static_fallbacks.items():
        if code not in material_rates:
            material_rates[code] = data
    
    return material_rates
