import { render, screen, fireEvent } from '@testing-library/react';
import { useNavigate } from 'react-router-dom';
import SearchBar from '../../components/SearchBar';

jest.mock('react-router-dom', () => ({
  ...jest.requireActual('react-router-dom'),
  useNavigate: jest.fn(),
}));

describe('SearchBar', () => {
  let navigateMock: jest.Mock;

  beforeEach(() => {
    navigateMock = jest.fn();
    (useNavigate as jest.Mock).mockReturnValue(navigateMock);
  });

  it('renders search bar with input and buttons', () => {
    render(<SearchBar />);
    expect(screen.getByRole('textbox')).toBeInTheDocument();
    expect(screen.getByText('Vietnamnet Search')).toBeInTheDocument();
  });

  it('updates input value on change', () => {
    render(<SearchBar />);
    const input = screen.getByRole('textbox');
    fireEvent.change(input, { target: { value: 'test' } });
    expect(input).toHaveValue('test');
  });

  it('clears input when clear button is clicked', () => {
    render(<SearchBar />);
    const input = screen.getByRole('textbox');
    fireEvent.change(input, { target: { value: 'test' } });
    fireEvent.click(screen.getByLabelText('Clear search'));
    expect(input).toHaveValue('');
  });

  it('navigates on form submit with valid query', () => {
    render(<SearchBar />);
    const input = screen.getByRole('textbox');
    fireEvent.change(input, { target: { value: 'test' } });
    fireEvent.submit(screen.getByTestId('search-form'));
    expect(navigateMock).toHaveBeenCalledWith('/search?q=test');
  });

  it('does not navigate on form submit with empty query', () => {
    render(<SearchBar />);
    const input = screen.getByRole('textbox');
    fireEvent.change(input, { target: { value: '' } });
    fireEvent.submit(screen.getByTestId('search-form'));
    expect(navigateMock).not.toHaveBeenCalled();
  });
});
