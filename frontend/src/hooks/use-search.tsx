import { useState } from 'react';
const API_URL = import.meta.env.VITE_API_URL || '/api';

export function useSearch() {
  const [results, setResults] = useState([]);
  const [query, setQuery] = useState('');
  const [loading, setLoading] = useState(false);
  const [page, setPage] = useState(1);
  const [limit, setLimit] = useState(10);
  const [total, setTotal] = useState(0);
  const [error, setError] = useState(null);
  const [time,setTime] = useState(0);

  const search = async (searchTerm: string, newPage = 1) => {
    setLoading(true);
    setError(null);
    try {
      const response = await fetch(`${API_URL}/search`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          query: searchTerm,
          page: newPage,
          limit,
        }),
      });

      if (!response.ok) throw new Error('Lỗi khi gọi API');

      const data = await response.json();
      setResults(data.results || []);
      setPage(data.page || 1);
      setLimit(data.limit || 10);
      setTotal(data.total || 0);
      setQuery(searchTerm);
      setTime(data.time || 0);
    } catch (err) {
      console.error(err);
      setError(err.message || 'Có lỗi xảy ra');
    } finally {
      setLoading(false);
    }
  };

  return { query, results, loading, error, search, page, setPage, limit, total,time };
}
