import { renderHook, act } from '@testing-library/react';
import { useIsMobile } from '../../hooks/use-mobile';

describe('useIsMobile', () => {
  beforeEach(() => {
    // Mock window.matchMedia
    Object.defineProperty(window, 'matchMedia', {
      writable: true,
      value: jest.fn().mockImplementation((query) => ({
        matches: false,
        media: query,
        onchange: null,
        addEventListener: jest.fn(),
        removeEventListener: jest.fn(),
        addListener: jest.fn(), // Deprecated
        removeListener: jest.fn(), // Deprecated
        dispatchEvent: jest.fn(),
      })),
    });
  });

  it('returns true when window width is less than 768px', () => {
    window.innerWidth = 600;
    const { result } = renderHook(() => useIsMobile());
    expect(result.current).toBe(true);
  });

  it('returns false when window width is greater than 768px', () => {
    window.innerWidth = 800;
    const { result } = renderHook(() => useIsMobile());
    expect(result.current).toBe(false);
  });

  it('updates state on window resize', () => {
    window.innerWidth = 800; // Bắt đầu với > 768px
    const { result } = renderHook(() => useIsMobile());
    act(() => {
      window.innerWidth = 600; // Thay đổi thành < 768px
      window.dispatchEvent(new Event('resize'));
    });
    expect(result.current).toBe(true);
  });
});