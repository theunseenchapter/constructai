#!/usr/bin/env python3
"""
Database initialization script for ConstructAI Dynamic Pricing System
Creates tables and populates initial material price data
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from core.config import settings
from core.pricing import MaterialPrice, Base, DynamicPricingSystem
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_pricing_database():
    """Initialize the pricing database tables and data"""
    try:
        # Create synchronous engine
        database_url = settings.database_url.replace("postgresql+asyncpg://", "postgresql://")
        engine = create_engine(database_url, echo=True)
        
        # Create tables
        logger.info("Creating pricing database tables...")
        Base.metadata.create_all(bind=engine)
        
        # Create session
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = SessionLocal()
        
        try:
            # Initialize pricing system with default materials
            logger.info("Initializing pricing system with default materials...")
            pricing_system = DynamicPricingSystem(db)
            
            # Check if initialization was successful
            current_prices = pricing_system.get_current_prices()
            logger.info(f"✅ Successfully initialized {len(current_prices)} materials")
            
            # Print summary
            for code, data in current_prices.items():
                logger.info(f"  - {code}: ₹{data['rate']}/{data['unit']} ({data['material_name']})")
            
        except Exception as e:
            db.rollback()
            logger.error(f"Error initializing pricing data: {str(e)}")
            raise
        finally:
            db.close()
        
        logger.info("✅ Pricing database initialization completed successfully!")
        return True
        
    except Exception as e:
        logger.error(f"❌ Database initialization failed: {str(e)}")
        return False

def test_pricing_system():
    """Test the pricing system functionality"""
    try:
        # Create session
        database_url = settings.database_url.replace("postgresql+asyncpg://", "postgresql://")
        engine = create_engine(database_url)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = SessionLocal()
        
        try:
            pricing_system = DynamicPricingSystem(db)
            
            # Test basic functionality
            logger.info("🧪 Testing pricing system functionality...")
            
            # Get current prices
            prices = pricing_system.get_current_prices()
            logger.info(f"✅ Retrieved {len(prices)} material prices")
            
            # Get market summary
            summary = pricing_system.get_market_summary()
            logger.info(f"✅ Market summary: {summary.get('total_materials', 0)} materials tracked")
            
            # Test price update
            result = pricing_system.update_material_price("cement_opc_53", 425.0, "test")
            if result.get("updated"):
                logger.info("✅ Price update test successful")
            else:
                logger.warning("⚠️ Price update test failed")
            
        except Exception as e:
            logger.error(f"❌ Pricing system test failed: {str(e)}")
            return False
        finally:
            db.close()
        
        logger.info("✅ All pricing system tests passed!")
        return True
        
    except Exception as e:
        logger.error(f"❌ Pricing system test failed: {str(e)}")
        return False

if __name__ == "__main__":
    print("🚀 Initializing ConstructAI Dynamic Pricing System...")
    
    # Initialize database
    if init_pricing_database():
        # Test the system
        if test_pricing_system():
            print("🎉 Dynamic pricing system is ready!")
        else:
            print("⚠️ System initialized but tests failed")
            sys.exit(1)
    else:
        print("❌ Failed to initialize pricing system")
        sys.exit(1)
