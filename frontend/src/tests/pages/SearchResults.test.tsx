import { render, screen, fireEvent } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import { useSearch } from '../../hooks/use-search';
import SearchResults from '../../pages/SearchResults';

const mockNavigate = jest.fn();

jest.mock('react-router-dom', () => ({
  ...jest.requireActual('react-router-dom'),
  useLocation: jest.fn(() => ({ search: '?q=test' })),
  useNavigate: () => mockNavigate,
}));

jest.mock('../../hooks/use-search', () => ({
  useSearch: jest.fn(),
}));

describe('SearchResults Page', () => {
  const defaultMock = {
    results: [
      { url: 'http://example.com', title: 'Test Title', snippet: 'Test snippet' },
    ],
    loading: false,
    error: null,
    search: jest.fn(),
    page: 1,
    setPage: jest.fn(),
    limit: 10,
    total: 1,
    time: 0.1,
  };

  beforeEach(() => {
    (useSearch as jest.Mock).mockReturnValue(defaultMock);
    mockNavigate.mockReset();
  });

  it('hiển thị kết quả tìm kiếm', () => {
    render(
      <MemoryRouter initialEntries={['/search?q=test']}>
        <SearchResults />
      </MemoryRouter>
    );

    expect(screen.getByText('Kết quả tìm kiếm cho: test')).toBeInTheDocument();
    expect(screen.getByText('About 1 results (0.1s)')).toBeInTheDocument();
    expect(screen.getByText('Test Title')).toBeInTheDocument();
    expect(screen.getByText('Test snippet')).toBeInTheDocument();
  });

  it('hiển thị trạng thái loading', () => {
    (useSearch as jest.Mock).mockReturnValue({
      ...defaultMock,
      loading: true,
    });

    render(
      <MemoryRouter initialEntries={['/search?q=test']}>
        <SearchResults />
      </MemoryRouter>
    );

    expect(screen.getByRole('img')).toBeInTheDocument(); // Spinner SVG
  });

  it('hiển thị trạng thái lỗi', () => {
    (useSearch as jest.Mock).mockReturnValue({
      ...defaultMock,
      error: 'Lỗi server',
    });

    render(
      <MemoryRouter initialEntries={['/search?q=test']}>
        <SearchResults />
      </MemoryRouter>
    );

    expect(screen.getByText('Có lỗi xảy ra: Lỗi server')).toBeInTheDocument();
  });

  it('gửi form tìm kiếm và điều hướng đúng', () => {
    render(
      <MemoryRouter initialEntries={['/search?q=test']}>
        <SearchResults />
      </MemoryRouter>
    );

    const input = screen.getByRole('textbox') as HTMLInputElement;
    fireEvent.change(input, { target: { value: 'new query' } });
    fireEvent.submit(screen.getByTestId('search-form'));

    expect(mockNavigate).toHaveBeenCalledWith('/search?q=new%20query');
  });

  it('hiển thị phân trang khi có nhiều kết quả', () => {
    (useSearch as jest.Mock).mockReturnValue({
      ...defaultMock,
      total: 50,
    });

    render(
      <MemoryRouter initialEntries={['/search?q=test']}>
        <SearchResults />
      </MemoryRouter>
    );

    expect(screen.getByText('Previous')).toBeInTheDocument();
    expect(screen.getByText('Next')).toBeInTheDocument();
  });

  it('hiển thị thông báo khi không có kết quả', () => {
    (useSearch as jest.Mock).mockReturnValue({
      ...defaultMock,
      results: [],
    });

    render(
      <MemoryRouter initialEntries={['/search?q=none']}>
        <SearchResults />
      </MemoryRouter>
    );

    expect(screen.getByText('Không tìm thấy kết quả nào phù hợp.')).toBeInTheDocument();
  });
});
