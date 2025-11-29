import React, { useState, useEffect } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, AreaChart, Area } from 'recharts';
import { TrendingUp, TrendingDown, AlertCircle, RefreshCw, Calendar, DollarSign, Github, Mail, Heart } from 'lucide-react';

const API_BASE_URL = 'http://localhost:8000/api';

const GoldPriceAnalyzer = () => {
  const [loading, setLoading] = useState(true);
  const [priceData, setPriceData] = useState([]);
  const [latestPrice, setLatestPrice] = useState(null);
  const [tracking, setTracking] = useState(null);
  const [statistics, setStatistics] = useState(null);
  const [selectedPeriod, setSelectedPeriod] = useState('3months');
  const [viewMode, setViewMode] = useState('daily'); // 'daily', 'monthly', 'yearly'
  const [syncing, setSyncing] = useState(false);
  const [selectedCarat, setSelectedCarat] = useState('22'); // '22' or '24'

  const periods = [
    { value: 'month', label: '1 Month' },
    { value: '3months', label: '3 Months' },
    { value: '6months', label: '6 Months' },
    { value: 'year', label: '1 Year' },
    { value: 'all', label: 'All Time' }
  ];

  useEffect(() => {
    loadDashboardData();
  }, []);

  useEffect(() => {
    loadPriceData(selectedPeriod);
  }, [selectedPeriod, viewMode]);

  const loadDashboardData = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/dashboard`);
      const result = await response.json();

      if (result.status === 'success') {
        setLatestPrice(result.data.latest_price);
        setTracking(result.data.tracking);
        setStatistics(result.data.statistics);
      }
    } catch (error) {
      console.error('Error loading dashboard:', error);
      // Set empty defaults on error so the UI doesn't break
      setLatestPrice(null);
      setTracking(null);
      setStatistics(null);
    }
  };

  const loadPriceData = async (period) => {
    setLoading(true);
    try {
      let endpoint = '';
      
      if (viewMode === 'daily') {
        endpoint = `${API_BASE_URL}/prices/period/${period}`;
      } else if (viewMode === 'monthly') {
        endpoint = `${API_BASE_URL}/prices/monthly-aggregate`;
      } else if (viewMode === 'yearly') {
        endpoint = `${API_BASE_URL}/prices/yearly-aggregate`;
      }
      
      const response = await fetch(endpoint);
      const result = await response.json();
      
      if (result.status === 'success') {
        setPriceData(result.data);
      }
    } catch (error) {
      console.error('Error loading price data:', error);
    } finally {
      setLoading(false);
    }
  };

  const syncData = async () => {
    setSyncing(true);
    try {
      const response = await fetch(`${API_BASE_URL}/scrape/sync`, { method: 'POST' });
      const result = await response.json();
      
      if (result.status === 'success') {
        await loadDashboardData();
        await loadPriceData(selectedPeriod);
        alert(`Sync complete! ${result.data.new_records} new records added.`);
      }
    } catch (error) {
      console.error('Error syncing data:', error);
      alert('Error syncing data. Please try again.');
    } finally {
      setSyncing(false);
    }
  };

  const formatPrice = (price) => {
    return new Intl.NumberFormat('en-LK', {
      style: 'currency',
      currency: 'LKR',
      minimumFractionDigits: 2
    }).format(price);
  };

  const formatDate = (dateStr) => {
    if (viewMode === 'monthly') {
      // Format YYYY-MM to readable format
      const [year, month] = dateStr.split('-');
      const date = new Date(year, parseInt(month) - 1);
      return date.toLocaleDateString('en-US', { year: 'numeric', month: 'short' });
    } else if (viewMode === 'yearly') {
      return dateStr; // Already formatted as YYYY
    }

    // Daily view - format based on period
    const date = new Date(dateStr);

    if (selectedPeriod === 'month') {
      // Show day and month for 1 month view
      return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
    } else if (selectedPeriod === '3months' || selectedPeriod === '6months') {
      // Show month and day for 3-6 months
      return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
    } else if (selectedPeriod === 'year' || selectedPeriod === 'all') {
      // Show month and year for longer periods
      return date.toLocaleDateString('en-US', { year: '2-digit', month: 'short' });
    }

    return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
  };

  const getPriceFieldName = () => {
    // Get the correct price field based on selected carat and view mode
    if (viewMode === 'monthly' || viewMode === 'yearly') {
      return selectedCarat === '22' ? 'avg_carat_22_1gram' : 'avg_carat_24_1gram';
    } else {
      return selectedCarat === '22' ? 'carat_22_1gram' : 'carat_24_1gram';
    }
  };

  const getChartData = () => {
    if (!priceData || priceData.length === 0) return [];

    const priceField = getPriceFieldName();

    if (viewMode === 'monthly') {
      return priceData.map(item => ({
        date: item.month,
        price: item[priceField] || 0,
        min: item.min_price || 0,
        max: item.max_price || 0
      }));
    } else if (viewMode === 'yearly') {
      return priceData.map(item => ({
        date: item.year,
        price: item[priceField] || 0,
        min: item.min_price || 0,
        max: item.max_price || 0
      }));
    } else {
      return priceData.map(item => ({
        date: item.date,
        price: item[priceField] || 0
      }));
    }
  };

  const getAlertColor = (alert) => {
    if (alert.severity === 'critical') {
      return alert.data.alert_type === 'increase' ? 'bg-green-100 border-green-500' : 'bg-red-100 border-red-500';
    }
    return 'bg-blue-100 border-blue-500';
  };

  const getAlertIcon = (alert) => {
    if (alert.severity === 'critical') {
      return alert.data.alert_type === 'increase' ?
        <TrendingUp className="text-green-600" size={24} /> :
        <TrendingDown className="text-red-600" size={24} />;
    }
    return <AlertCircle className="text-blue-600" size={24} />;
  };

  const getXAxisInterval = () => {
    const dataLength = getChartData().length;

    if (viewMode === 'yearly') {
      return 0; // Show all years
    } else if (viewMode === 'monthly') {
      if (dataLength > 24) return Math.floor(dataLength / 12); // Show ~12 ticks
      if (dataLength > 12) return 1; // Show every other month
      return 0; // Show all months
    } else {
      // Daily view
      if (selectedPeriod === 'month') {
        return Math.max(0, Math.floor(dataLength / 10)); // Show ~10 ticks for 1 month
      } else if (selectedPeriod === '3months') {
        return Math.max(0, Math.floor(dataLength / 10)); // Show ~10 ticks
      } else if (selectedPeriod === '6months') {
        return Math.max(0, Math.floor(dataLength / 12)); // Show ~12 ticks
      } else if (selectedPeriod === 'year' || selectedPeriod === 'all') {
        return Math.max(0, Math.floor(dataLength / 15)); // Show ~15 ticks
      }
    }

    return 'preserveStartEnd';
  };

  const calculateStatistics = () => {
    if (!priceData || priceData.length === 0) return null;

    const chartData = getChartData();
    if (chartData.length === 0) return null;

    const prices = chartData.map(item => item.price).filter(p => p > 0);
    if (prices.length === 0) return null;

    const currentPrice = prices[prices.length - 1];
    const startPrice = prices[0];
    const minPrice = Math.min(...prices);
    const maxPrice = Math.max(...prices);
    const avgPrice = prices.reduce((sum, p) => sum + p, 0) / prices.length;
    const priceChange = currentPrice - startPrice;
    const priceChangePercentage = startPrice > 0 ? (priceChange / startPrice) * 100 : 0;

    return {
      current_price: currentPrice,
      min_price: minPrice,
      max_price: maxPrice,
      avg_price: avgPrice,
      price_change: priceChange,
      price_change_percentage: priceChangePercentage
    };
  };

  // Show loading screen on initial load
  if (loading && !latestPrice && !priceData.length) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-amber-50 via-yellow-50 to-orange-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-b-4 border-amber-600 mx-auto mb-4"></div>
          <p className="text-xl text-gray-600">Loading Gold Price Analyzer...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-amber-50 via-yellow-50 to-orange-50">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="bg-gradient-to-r from-amber-600 to-yellow-600 rounded-2xl shadow-2xl p-8 mb-8 text-white">
          <div className="flex justify-between items-center flex-wrap gap-4">
            <div>
              <h1 className="text-4xl font-bold mb-2 flex items-center gap-3">
                <DollarSign size={40} />
                Gold Price Analyzer
              </h1>
              <p className="text-amber-100">Real-time Gold Price Tracking</p>
            </div>
            <div className="flex gap-4 items-center">
              {/* Carat Selector */}
              <div className="bg-white/10 backdrop-blur-sm rounded-xl p-1 flex gap-1">
                <button
                  onClick={() => setSelectedCarat('22')}
                  className={`px-6 py-2 rounded-lg font-semibold transition-all ${
                    selectedCarat === '22'
                      ? 'bg-white text-amber-600 shadow-lg'
                      : 'text-white hover:bg-white/20'
                  }`}
                >
                  22 Carat
                </button>
                <button
                  onClick={() => setSelectedCarat('24')}
                  className={`px-6 py-2 rounded-lg font-semibold transition-all ${
                    selectedCarat === '24'
                      ? 'bg-white text-amber-600 shadow-lg'
                      : 'text-white hover:bg-white/20'
                  }`}
                >
                  24 Carat
                </button>
              </div>
              <button
                onClick={syncData}
                disabled={syncing}
                className="bg-white text-amber-600 px-6 py-3 rounded-xl font-semibold hover:bg-amber-50 transition-all flex items-center gap-2 shadow-lg disabled:opacity-50"
              >
                <RefreshCw className={syncing ? 'animate-spin' : ''} size={20} />
                {syncing ? 'Syncing...' : 'Sync Data'}
              </button>
            </div>
          </div>
        </div>

        {/* Latest Price Card */}
        {latestPrice && (
          <div className="bg-white rounded-2xl shadow-xl p-6 mb-8">
            <h2 className="text-2xl font-bold text-gray-800 mb-4">
              Current Gold Price ({selectedCarat} Carat)
            </h2>
            {selectedCarat === '22' ? (
              <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                <div className="bg-gradient-to-br from-amber-400 to-yellow-500 rounded-xl p-6 text-white">
                  <p className="text-sm opacity-90 mb-1">22 Carat 1 Gram</p>
                  <p className="text-3xl font-bold">{formatPrice(latestPrice.carat_22_1gram)}</p>
                </div>
                <div className="bg-gradient-to-br from-amber-500 to-orange-500 rounded-xl p-6 text-white">
                  <p className="text-sm opacity-90 mb-1">22 Carat 8 Grams (1 Pawn)</p>
                  <p className="text-3xl font-bold">{formatPrice(latestPrice.carat_22_8grams)}</p>
                </div>
                <div className="bg-gradient-to-br from-yellow-500 to-amber-600 rounded-xl p-6 text-white">
                  <p className="text-sm opacity-90 mb-1">21 Carat 1 Gram</p>
                  <p className="text-3xl font-bold">{formatPrice(latestPrice.carat_21_1gram)}</p>
                </div>
                <div className="bg-gradient-to-br from-orange-500 to-red-500 rounded-xl p-6 text-white">
                  <p className="text-sm opacity-90 mb-1">Gold Ounce</p>
                  <p className="text-3xl font-bold">{formatPrice(latestPrice.gold_ounce)}</p>
                </div>
              </div>
            ) : (
              <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                <div className="bg-gradient-to-br from-yellow-400 to-amber-500 rounded-xl p-6 text-white">
                  <p className="text-sm opacity-90 mb-1">24 Carat 1 Gram</p>
                  <p className="text-3xl font-bold">{formatPrice(latestPrice.carat_24_1gram)}</p>
                </div>
                <div className="bg-gradient-to-br from-amber-500 to-yellow-600 rounded-xl p-6 text-white">
                  <p className="text-sm opacity-90 mb-1">24 Carat 8 Grams (1 Pawn)</p>
                  <p className="text-3xl font-bold">{formatPrice(latestPrice.carat_24_1gram * 8)}</p>
                </div>
                <div className="bg-gradient-to-br from-yellow-500 to-orange-500 rounded-xl p-6 text-white">
                  <p className="text-sm opacity-90 mb-1">22 Carat 1 Gram</p>
                  <p className="text-3xl font-bold">{formatPrice(latestPrice.carat_22_1gram)}</p>
                </div>
                <div className="bg-gradient-to-br from-orange-500 to-red-500 rounded-xl p-6 text-white">
                  <p className="text-sm opacity-90 mb-1">Gold Ounce</p>
                  <p className="text-3xl font-bold">{formatPrice(latestPrice.gold_ounce)}</p>
                </div>
              </div>
            )}
            <p className="text-sm text-gray-500 mt-4 flex items-center gap-2">
              <Calendar size={16} />
              Last updated: {new Date(latestPrice.date).toLocaleDateString('en-US', {
                year: 'numeric', month: 'long', day: 'numeric'
              })}
            </p>
          </div>
        )}

        {/* Price Alerts */}
        {(() => {
          // Get alerts for the selected carat
          const caratKey = `carat_${selectedCarat}`;
          const caratAlerts = tracking && tracking[caratKey] ? tracking[caratKey].alerts : [];

          return caratAlerts && caratAlerts.length > 0 && (
            <div className="bg-white rounded-2xl shadow-xl p-6 mb-8">
              <div className="flex justify-between items-center mb-4">
                <h2 className="text-2xl font-bold text-gray-800">
                  Price Alerts - {selectedCarat} Carat
                </h2>
              </div>
              <div className="space-y-4">
                {caratAlerts.map((alert, index) => (
                  <div
                    key={index}
                    className={`border-l-4 rounded-lg p-4 flex items-start gap-4 ${getAlertColor(alert)}`}
                  >
                    {getAlertIcon(alert)}
                    <div className="flex-1">
                      <p className="font-semibold text-gray-800">{alert.message}</p>
                      <div className="mt-2 text-sm text-gray-600">
                        <p>Period: {alert.data.period_type === 'week' ? '7 days' : '30 days'}</p>
                        <p>Base Price: {formatPrice(alert.data.base_price)} → Current: {formatPrice(alert.data.current_price)}</p>
                        <p>Change: {formatPrice(alert.data.price_change)} ({alert.data.percentage_change > 0 ? '+' : ''}{alert.data.percentage_change}%)</p>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          );
        })()}

        {/* Chart Controls */}
        <div className="bg-white rounded-2xl shadow-xl p-6 mb-8">
          <div className="flex flex-wrap gap-4 items-center justify-between">
            <div>
              <h2 className="text-2xl font-bold text-gray-800 mb-4">Price History</h2>
              <div className="flex gap-2 flex-wrap">
                {periods.map(period => (
                  <button
                    key={period.value}
                    onClick={() => setSelectedPeriod(period.value)}
                    className={`px-4 py-2 rounded-lg font-medium transition-all ${
                      selectedPeriod === period.value
                        ? 'bg-amber-600 text-white shadow-lg'
                        : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                    }`}
                  >
                    {period.label}
                  </button>
                ))}
              </div>
            </div>
            
            <div>
              <p className="text-sm text-gray-600 mb-2">View Mode</p>
              <div className="flex gap-2">
                <button
                  onClick={() => { setViewMode('daily'); loadPriceData(selectedPeriod); }}
                  className={`px-4 py-2 rounded-lg font-medium transition-all ${
                    viewMode === 'daily'
                      ? 'bg-blue-600 text-white'
                      : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                  }`}
                >
                  Daily
                </button>
                <button
                  onClick={() => { setViewMode('monthly'); loadPriceData(selectedPeriod); }}
                  className={`px-4 py-2 rounded-lg font-medium transition-all ${
                    viewMode === 'monthly'
                      ? 'bg-blue-600 text-white'
                      : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                  }`}
                >
                  Monthly
                </button>
                <button
                  onClick={() => { setViewMode('yearly'); loadPriceData(selectedPeriod); }}
                  className={`px-4 py-2 rounded-lg font-medium transition-all ${
                    viewMode === 'yearly'
                      ? 'bg-blue-600 text-white'
                      : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                  }`}
                >
                  Yearly
                </button>
              </div>
            </div>
          </div>

          {/* Chart */}
          <div className="mt-8">
            {loading ? (
              <div className="flex items-center justify-center h-96">
                <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-amber-600"></div>
              </div>
            ) : (
              <ResponsiveContainer width="100%" height={400}>
                <AreaChart data={getChartData()}>
                  <defs>
                    <linearGradient id="colorPrice" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#f59e0b" stopOpacity={0.8}/>
                      <stop offset="95%" stopColor="#f59e0b" stopOpacity={0}/>
                    </linearGradient>
                  </defs>
                  <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
                  <XAxis
                    dataKey="date"
                    tickFormatter={formatDate}
                    stroke="#6b7280"
                    angle={-45}
                    textAnchor="end"
                    height={80}
                    interval={getXAxisInterval()}
                    tick={{ fontSize: 12 }}
                  />
                  <YAxis 
                    stroke="#6b7280"
                    tickFormatter={(value) => `Rs. ${(value / 1000).toFixed(0)}k`}
                  />
                  <Tooltip 
                    formatter={(value) => formatPrice(value)}
                    labelFormatter={formatDate}
                    contentStyle={{ 
                      backgroundColor: 'rgba(255, 255, 255, 0.95)', 
                      border: '1px solid #e5e7eb',
                      borderRadius: '8px'
                    }}
                  />
                  <Legend />
                  <Area
                    type="monotone"
                    dataKey="price"
                    stroke="#f59e0b"
                    strokeWidth={3}
                    fillOpacity={1}
                    fill="url(#colorPrice)"
                    name={`${selectedCarat} Carat 1 Gram`}
                  />
                  {viewMode !== 'daily' && (
                    <>
                      <Line type="monotone" dataKey="min" stroke="#ef4444" strokeWidth={2} dot={false} name="Min Price" />
                      <Line type="monotone" dataKey="max" stroke="#10b981" strokeWidth={2} dot={false} name="Max Price" />
                    </>
                  )}
                </AreaChart>
              </ResponsiveContainer>
            )}
          </div>
        </div>

        {/* Statistics */}
        {(() => {
          const stats = calculateStatistics();
          return stats && (
            <div className="bg-white rounded-2xl shadow-xl p-6">
              <h2 className="text-2xl font-bold text-gray-800 mb-4">
                Statistics - {selectedCarat} Carat ({selectedPeriod})
              </h2>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                <div className="bg-gradient-to-br from-blue-50 to-blue-100 rounded-xl p-4">
                  <p className="text-sm text-blue-600 font-medium mb-1">Current Price</p>
                  <p className="text-2xl font-bold text-blue-900">{formatPrice(stats.current_price)}</p>
                </div>
                <div className="bg-gradient-to-br from-green-50 to-green-100 rounded-xl p-4">
                  <p className="text-sm text-green-600 font-medium mb-1">Average Price</p>
                  <p className="text-2xl font-bold text-green-900">{formatPrice(stats.avg_price)}</p>
                </div>
                <div className="bg-gradient-to-br from-purple-50 to-purple-100 rounded-xl p-4">
                  <p className="text-sm text-purple-600 font-medium mb-1">Min Price</p>
                  <p className="text-2xl font-bold text-purple-900">{formatPrice(stats.min_price)}</p>
                </div>
                <div className="bg-gradient-to-br from-orange-50 to-orange-100 rounded-xl p-4">
                  <p className="text-sm text-orange-600 font-medium mb-1">Max Price</p>
                  <p className="text-2xl font-bold text-orange-900">{formatPrice(stats.max_price)}</p>
                </div>
              </div>
              <div className="mt-4 bg-gray-50 rounded-xl p-4">
                <p className="text-sm text-gray-600">Price Change in Period</p>
                <p className={`text-3xl font-bold ${(stats.price_change || 0) >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                  {(stats.price_change || 0) >= 0 ? '+' : ''}{formatPrice(stats.price_change || 0)}
                  <span className="text-lg ml-2">
                    ({(stats.price_change_percentage || 0) >= 0 ? '+' : ''}{(stats.price_change_percentage || 0).toFixed(2)}%)
                  </span>
                </p>
              </div>
            </div>
          );
        })()}
      </div>

      {/* Footer */}
      <footer className="bg-gradient-to-r from-gray-900 via-gray-800 to-gray-900 text-white mt-16">
        <div className="container mx-auto px-4 py-8">
          <div className="flex flex-col items-center text-center">
            {/* About Section */}
            <div className="mb-6">
              <h3 className="text-2xl font-bold mb-3 flex items-center justify-center gap-2">
                <DollarSign size={28} className="text-amber-400" />
                Gold Price Analyzer
              </h3>
              <p className="text-gray-400 text-sm leading-relaxed max-w-2xl">
                A comprehensive multi-agent system for tracking and analyzing gold prices in Sri Lanka.
                Real-time data synchronization, intelligent alerts, and detailed analytics.
              </p>
            </div>

            {/* Copyright */}
            <div className="border-t border-gray-700 pt-6 w-full">
              <p className="text-gray-400 text-sm">
                &copy; {new Date().getFullYear()} Team Inferno. All rights reserved.
              </p>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default GoldPriceAnalyzer;
