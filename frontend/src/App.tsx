import React, { useState } from "react";
const App: React.FC = () => {
  const [trends, setTrends] = useState<string[]>([]);
  const [recentTrends, setRecentTrends] = useState<string[]>([]);
  const [loading, setLoading] = useState(false);
  const [fetchingRecent, setFetchingRecent] = useState(false);
  const [recentMessage, setRecentMessage] = useState<string | null>(null);

  const scrapeTrends = async () => {
    setLoading(true);
    setTrends([]);

    try {
      const response = await fetch("/scrape", {
        method: "POST",
      });
      if (response.ok) {
        const data = await response.json();
        setTrends(data.trends || []);
      } else {
        alert("Failed to fetch trends. Please try again.");
      }
    } catch (error) {
      console.error("Error:", error);
      alert("An error occurred while fetching trends.");
    } finally {
      setLoading(false);
    }
  };

  const fetchRecentTrends = async () => {
    setFetchingRecent(true);
    setRecentTrends([]);
    setRecentMessage(null);

    try {
      const response = await fetch("/recent-trends", {
        method: "GET",
      });
      if (response.ok) {
        const data = await response.json();
        if (data.trends.length === 0) {
          setRecentMessage(data.message || "No trends available.");
        } else {
          setRecentTrends(data.trends);
        }
      } else {
        alert("Failed to fetch recent trends. Please try again.");
      }
    } catch (error) {
      console.error("Error:", error);
      alert("An error occurred while fetching recent trends.");
    } finally {
      setFetchingRecent(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center p-4">
      <div className="bg-white p-6 rounded-lg shadow-lg max-w-xl w-full">
        <h1 className="text-2xl font-bold text-center text-blue-500 mb-6">
          Twitter Trend Scraper
        </h1>
        <button
          onClick={scrapeTrends}
          disabled={loading}
          className={`${
            loading ? "bg-gray-400 cursor-not-allowed" : "bg-blue-500"
          } text-white py-2 px-4 rounded-full w-full transition duration-300 hover:bg-blue-600 mb-4`}
        >
          {loading ? "Scraping..." : "Scrape Trending Topics"}
        </button>
        <ul className="mt-4 space-y-2">
          {trends.map((trend, index) => (
            <li
              key={index}
              className="p-2 border-b border-gray-300 text-gray-800"
            >
              {trend}
            </li>
          ))}
        </ul>
        <button
          onClick={fetchRecentTrends}
          disabled={fetchingRecent}
          className={`${
            fetchingRecent ? "bg-gray-400 cursor-not-allowed" : "bg-green-500"
          } text-white py-2 px-4 rounded-full w-full transition duration-300 hover:bg-green-600 mt-6`}
        >
          {fetchingRecent ? "Fetching..." : "Fetch Recent Trends"}
        </button>
        {recentMessage && (
          <p className="text-center text-gray-600 mt-4">{recentMessage}</p>
        )}
        <ul className="mt-4 space-y-2">
          {recentTrends.map((trend, index) => (
            <li
              key={index}
              className="p-2 border-b border-gray-300 text-gray-800"
            >
              {trend}
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default App;
