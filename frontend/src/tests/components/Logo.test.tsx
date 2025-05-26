import { render, screen } from '@testing-library/react';
import Logo from '../../components/Logo';

describe('Logo', () => {
  it('renders logo with default size', () => {
    render(<Logo />);
    const img = screen.getByAltText('Company Logo');
    expect(img).toHaveClass('w-80 h-24 object-contain');
    expect(img).toHaveAttribute('src', '/logo.png');
  });

  it('renders logo with small size', () => {
    render(<Logo small />);
    const img = screen.getByAltText('Company Logo');
    expect(img).toHaveClass('w-32 h-10 object-contain');
    expect(img).toHaveAttribute('src', '/logo.png');
  });
});