import React, { useState } from "react";

const App: React.FC = () => {
  const [cookies, setCookies] = useState("");
  const [trends, setTrends] = useState<string[]>([]);
  const [loading, setLoading] = useState(false);
  const [cookiesSaved, setCookiesSaved] = useState(false);

  const handleCookiesSubmit = async () => {
    try {
      const response = await fetch("/save-cookies", {
        method: "POST",
        headers: {
          "Content-Type": "text/plain",
        },
        body: cookies,
      });

      if (response.ok) {
        alert("Cookies saved successfully!");
        setCookiesSaved(true);
      } else {
        alert("Failed to save cookies. Please try again.");
      }
    } catch (error) {
      console.error("Error:", error);
      alert("An error occurred while saving cookies.");
    }
  };

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
        alert("Failed to fetch trends. Ensure cookies are saved.");
      }
    } catch (error) {
      console.error("Error:", error);
      alert("An error occurred while fetching trends.");
    } finally {
      setLoading(false);
    }
  };

  const fetchRecentTrends = async () => {
    setLoading(true);
    try {
      const response = await fetch("/recent-trends");
      if (response.ok) {
        const data = await response.json();
        setTrends(data.trends || []);
      } else {
        alert("Failed to fetch recent trends.");
      }
    } catch (error) {
      console.error("Error:", error);
      alert("An error occurred while fetching recent trends.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center p-4">
      <div className="bg-white p-6 rounded-lg shadow-lg max-w-xl w-full">
        <h1 className="text-2xl font-bold text-center text-blue-500 mb-6">
          Twitter Trend Scraper
        </h1>
        {!cookiesSaved ? (
          <div>
            <textarea
              value={cookies}
              onChange={(e) => setCookies(e.target.value)}
              placeholder="Paste Netscape cookies here..."
              className="w-full p-2 border rounded mb-4"
              rows={8}
            />
            <button
              onClick={handleCookiesSubmit}
              className="bg-green-500 text-white py-2 px-4 rounded-full w-full transition duration-300 hover:bg-green-600"
            >
              Save Cookies
            </button>
          </div>
        ) : (
          <div className="space-y-4">
            <button
              onClick={scrapeTrends}
              disabled={loading}
              className={`${
                loading ? "bg-gray-400 cursor-not-allowed" : "bg-blue-500"
              } text-white py-2 px-4 rounded-full w-full transition duration-300 hover:bg-blue-600`}
            >
              {loading ? "Loading..." : "Scrape Trending Topics"}
            </button>
            <button
              onClick={fetchRecentTrends}
              disabled={loading}
              className={`${
                loading ? "bg-gray-400 cursor-not-allowed" : "bg-purple-500"
              } text-white py-2 px-4 rounded-full w-full transition duration-300 hover:bg-purple-600`}
            >
              Fetch Recent Trends
            </button>
          </div>
        )}
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
      </div>
    </div>
  );
};

export default App;