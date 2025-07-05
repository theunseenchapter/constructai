'use client';

import { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Badge } from '@/components/ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { TrendingUp, TrendingDown, Minus, RefreshCw, DollarSign, BarChart3 } from 'lucide-react';

interface MaterialPrice {
  material_name: string;
  rate: number;
  unit: string;
  last_updated: string;
  fluctuation_percentage: number;
  market_trend: 'rising' | 'falling' | 'stable';
  weight_kg: number;
}

interface MarketSummary {
  total_materials: number;
  market_trends: {
    rising: number;
    falling: number;
    stable: number;
  };
  average_fluctuation: number;
  most_volatile_material: {
    code: string;
    name: string;
    fluctuation: number;
  };
  last_update: string;
}

export default function PricingAdminPage() {
  const [prices, setPrices] = useState<Record<string, MaterialPrice>>({});
  const [marketSummary, setMarketSummary] = useState<MarketSummary | null>(null);
  const [loading, setLoading] = useState(true);
  const [updating, setUpdating] = useState(false);
  const [editingPrice, setEditingPrice] = useState<{code: string, newPrice: string} | null>(null);

  useEffect(() => {
    fetchPrices();
    fetchMarketSummary();
  }, []);

  const fetchPrices = async () => {
    try {
      const response = await fetch('/api/v1/pricing/current-prices');
      const data = await response.json();
      if (data.success) {
        setPrices(data.prices);
      }
    } catch (error) {
      console.error('Error fetching prices:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchMarketSummary = async () => {
    try {
      const response = await fetch('/api/v1/pricing/market-summary');
      const data = await response.json();
      if (data.success) {
        setMarketSummary(data.data);
      }
    } catch (error) {
      console.error('Error fetching market summary:', error);
    }
  };

  const refreshLivePrices = async () => {
    setUpdating(true);
    try {
      const response = await fetch('/api/v1/pricing/refresh-live-prices', {
        method: 'POST'
      });
      const data = await response.json();
      if (data.success) {
        // Wait a moment for background update to complete
        setTimeout(() => {
          fetchPrices();
          fetchMarketSummary();
        }, 2000);
      }
    } catch (error) {
      console.error('Error refreshing prices:', error);
    } finally {
      setUpdating(false);
    }
  };

  const updatePrice = async (materialCode: string, newPrice: number) => {
    try {
      const response = await fetch('/api/v1/pricing/update-price', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          material_code: materialCode,
          new_price: newPrice,
          source: 'admin_manual'
        })
      });
      
      const data = await response.json();
      if (data.success) {
        fetchPrices();
        fetchMarketSummary();
        setEditingPrice(null);
      }
    } catch (error) {
      console.error('Error updating price:', error);
    }
  };

  const getTrendIcon = (trend: string) => {
    switch (trend) {
      case 'rising':
        return <TrendingUp className="h-4 w-4 text-green-500" />;
      case 'falling':
        return <TrendingDown className="h-4 w-4 text-red-500" />;
      default:
        return <Minus className="h-4 w-4 text-gray-500" />;
    }
  };

  const getTrendColor = (trend: string) => {
    switch (trend) {
      case 'rising':
        return 'bg-green-100 text-green-800';
      case 'falling':
        return 'bg-red-100 text-red-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('en-IN', {
      style: 'currency',
      currency: 'INR',
      minimumFractionDigits: 0,
      maximumFractionDigits: 2
    }).format(amount);
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  return (
    <div className="container mx-auto p-6 space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Material Pricing Dashboard</h1>
          <p className="text-gray-600 mt-2">Real-time construction material price management</p>
        </div>
        <Button 
          onClick={refreshLivePrices} 
          disabled={updating}
          className="bg-blue-600 hover:bg-blue-700"
        >
          <RefreshCw className={`h-4 w-4 mr-2 ${updating ? 'animate-spin' : ''}`} />
          {updating ? 'Updating...' : 'Refresh Live Prices'}
        </Button>
      </div>

      {/* Market Summary Cards */}
      {marketSummary && (
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <Card>
            <CardContent className="p-6">
              <div className="flex items-center">
                <DollarSign className="h-8 w-8 text-blue-600" />
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-600">Total Materials</p>
                  <p className="text-2xl font-bold text-gray-900">{marketSummary.total_materials}</p>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="p-6">
              <div className="flex items-center">
                <TrendingUp className="h-8 w-8 text-green-600" />
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-600">Rising Prices</p>
                  <p className="text-2xl font-bold text-green-600">{marketSummary.market_trends.rising}</p>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="p-6">
              <div className="flex items-center">
                <TrendingDown className="h-8 w-8 text-red-600" />
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-600">Falling Prices</p>
                  <p className="text-2xl font-bold text-red-600">{marketSummary.market_trends.falling}</p>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="p-6">
              <div className="flex items-center">
                <BarChart3 className="h-8 w-8 text-purple-600" />
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-600">Avg. Fluctuation</p>
                  <p className="text-2xl font-bold text-purple-600">{marketSummary.average_fluctuation.toFixed(2)}%</p>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      )}

      <Tabs defaultValue="materials" className="space-y-4">
        <TabsList>
          <TabsTrigger value="materials">Material Prices</TabsTrigger>
          <TabsTrigger value="trends">Market Trends</TabsTrigger>
        </TabsList>

        <TabsContent value="materials" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Current Material Prices</CardTitle>
              <CardDescription>
                Real-time material prices with market trends and fluctuation data
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="grid gap-4">
                {Object.entries(prices).map(([code, material]) => (
                  <div key={code} className="flex items-center justify-between p-4 border rounded-lg hover:bg-gray-50">
                    <div className="flex-1">
                      <div className="flex items-center gap-3">
                        <h3 className="font-semibold text-gray-900">{material.material_name}</h3>
                        <Badge className={getTrendColor(material.market_trend)}>
                          {getTrendIcon(material.market_trend)}
                          <span className="ml-1">{material.market_trend}</span>
                        </Badge>
                      </div>
                      <p className="text-sm text-gray-600 mt-1">
                        Code: {code} • Unit: {material.unit} • Weight: {material.weight_kg}kg
                      </p>
                      <p className="text-xs text-gray-500 mt-1">
                        Last updated: {new Date(material.last_updated).toLocaleString()}
                      </p>
                    </div>

                    <div className="flex items-center gap-4">
                      <div className="text-right">
                        {editingPrice?.code === code ? (
                          <div className="flex items-center gap-2">
                            <Input
                              type="number"
                              value={editingPrice.newPrice}
                              onChange={(e) => setEditingPrice({...editingPrice, newPrice: e.target.value})}
                              className="w-24 h-8"
                            />
                            <Button
                              size="sm"
                              onClick={() => updatePrice(code, parseFloat(editingPrice.newPrice))}
                            >
                              Save
                            </Button>
                            <Button
                              size="sm"
                              variant="outline"
                              onClick={() => setEditingPrice(null)}
                            >
                              Cancel
                            </Button>
                          </div>
                        ) : (
                          <>
                            <p className="text-lg font-bold text-gray-900">
                              {formatCurrency(material.rate)}
                            </p>
                            <p className="text-sm text-gray-600">per {material.unit}</p>
                            <Button
                              size="sm"
                              variant="outline"
                              onClick={() => setEditingPrice({code, newPrice: material.rate.toString()})}
                              className="mt-1"
                            >
                              Edit
                            </Button>
                          </>
                        )}
                      </div>

                      <div className="text-right min-w-[80px]">
                        <div className={`text-sm font-medium ${
                          material.fluctuation_percentage > 0 ? 'text-green-600' : 
                          material.fluctuation_percentage < 0 ? 'text-red-600' : 'text-gray-600'
                        }`}>
                          {material.fluctuation_percentage > 0 ? '+' : ''}{material.fluctuation_percentage.toFixed(2)}%
                        </div>
                        <div className="text-xs text-gray-500">24h change</div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="trends" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Market Analysis</CardTitle>
              <CardDescription>
                Detailed market trends and volatility analysis
              </CardDescription>
            </CardHeader>
            <CardContent>
              {marketSummary && (
                <div className="space-y-6">
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <div className="text-center p-4 bg-green-50 rounded-lg">
                      <TrendingUp className="h-8 w-8 text-green-600 mx-auto mb-2" />
                      <p className="text-2xl font-bold text-green-600">{marketSummary.market_trends.rising}</p>
                      <p className="text-sm text-green-700">Materials Rising</p>
                    </div>
                    <div className="text-center p-4 bg-red-50 rounded-lg">
                      <TrendingDown className="h-8 w-8 text-red-600 mx-auto mb-2" />
                      <p className="text-2xl font-bold text-red-600">{marketSummary.market_trends.falling}</p>
                      <p className="text-sm text-red-700">Materials Falling</p>
                    </div>
                    <div className="text-center p-4 bg-gray-50 rounded-lg">
                      <Minus className="h-8 w-8 text-gray-600 mx-auto mb-2" />
                      <p className="text-2xl font-bold text-gray-600">{marketSummary.market_trends.stable}</p>
                      <p className="text-sm text-gray-700">Materials Stable</p>
                    </div>
                  </div>

                  <div className="p-4 bg-yellow-50 rounded-lg">
                    <h4 className="font-semibold text-yellow-800 mb-2">Most Volatile Material</h4>
                    <p className="text-yellow-700">
                      <strong>{marketSummary.most_volatile_material.name}</strong> ({marketSummary.most_volatile_material.code})
                    </p>
                    <p className="text-yellow-600 text-sm">
                      Fluctuation: {marketSummary.most_volatile_material.fluctuation.toFixed(2)}%
                    </p>
                  </div>
                </div>
              )}
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
}
