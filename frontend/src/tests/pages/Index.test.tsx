import { render, screen } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import Index from '../../pages/Index';

describe('Index', () => {
  it('renders logo and search bar', () => {
    render(
      <BrowserRouter>
        <Index />
      </BrowserRouter>
    );
    expect(screen.getByAltText('Company Logo')).toBeInTheDocument();
    expect(screen.getByRole('textbox')).toBeInTheDocument();
  });

  it('sets document title to "Vietnamnet"', () => {
    render(
      <BrowserRouter>
        <Index />
      </BrowserRouter>
    );
    expect(document.title).toBe('Vietnamnet');
  });

  it('renders footer with copyright', () => {
    render(
      <BrowserRouter>
        <Index />
      </BrowserRouter>
    );
    expect(screen.getByText(/© \d{4} Copyright by AndreNguyen03&FhuAnn/)).toBeInTheDocument();
  });
});