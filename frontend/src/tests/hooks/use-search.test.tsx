import { renderHook, act, waitFor } from '@testing-library/react';
import { useSearch } from '../../hooks/use-search';

describe('useSearch', () => {
  beforeEach(() => {
    // Mock globalThis.fetch trước mỗi test
    globalThis.fetch = jest.fn();
  });

  afterEach(() => {
    // Reset mock sau mỗi test để tránh ảnh hưởng qua lại
    jest.resetAllMocks();
  });

  it('fetches search results successfully', async () => {
    const mockResponse = {
      results: [{ url: 'http://example.com', title: 'Test', snippet: 'Snippet' }],
      total: 1,
      page: 1,
      limit: 10,
      time: 0.1,
    };
    (globalThis.fetch as jest.Mock).mockResolvedValueOnce({
      ok: true,
      json: async () => mockResponse,
    });

    const { result } = renderHook(() => useSearch());
    await act(async () => {
      await result.current.search('test', 1);
    });

    expect(globalThis.fetch).toHaveBeenCalledWith('http://localhost:8000/search', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query: 'test', page: 1, limit: 10 }),
    });
    expect(result.current.results).toEqual(mockResponse.results);
    expect(result.current.total).toBe(1);
    expect(result.current.page).toBe(1);
    expect(result.current.time).toBe(0.1);
    expect(result.current.loading).toBe(false);
    expect(result.current.error).toBe(null);
  });

  it('handles API error', async () => {
    (globalThis.fetch as jest.Mock).mockResolvedValueOnce({
      ok: false,
    });

    const { result } = renderHook(() => useSearch());
    await act(async () => {
      await result.current.search('test', 1);
    });

    expect(result.current.error).toBe('Lỗi khi gọi API');
    expect(result.current.results).toEqual([]);  // Kết quả phải reset về []
    expect(result.current.loading).toBe(false);
  });

  it('sets loading state during fetch', async () => {
    (globalThis.fetch as jest.Mock).mockImplementationOnce(
      () =>
        new Promise((resolve) =>
          setTimeout(() => resolve({ ok: true, json: async () => ({}) }), 100)
        )
    );

    const { result } = renderHook(() => useSearch());

    act(() => {
      result.current.search('test', 1);
    });

    expect(result.current.loading).toBe(true);

    await waitFor(() => expect(result.current.loading).toBe(false));
  });

  it('updates page state', () => {
    const { result } = renderHook(() => useSearch());
    act(() => {
      result.current.setPage(2);
    });
    expect(result.current.page).toBe(2);
  });
});
