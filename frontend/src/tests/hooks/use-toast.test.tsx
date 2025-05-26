import { renderHook, act } from '@testing-library/react';
import { useToast, toast } from '../../hooks/use-toast';

describe('useToast', () => {
  it('adds a toast and updates state', () => {
    const { result } = renderHook(() => useToast());
    act(() => {
      toast({ title: 'Test Toast', description: 'This is a test' });
    });
    expect(result.current.toasts).toHaveLength(1);
    expect(result.current.toasts[0].title).toBe('Test Toast');
    expect(result.current.toasts[0].description).toBe('This is a test');
  });

  it('limits toasts to TOAST_LIMIT (1)', () => {
    const { result } = renderHook(() => useToast());
    act(() => {
      toast({ title: 'Toast 1', description: 'First' });
      toast({ title: 'Toast 2', description: 'Second' });
    });
    expect(result.current.toasts).toHaveLength(1);
    expect(result.current.toasts[0].title).toBe('Toast 2');
  });

  it('dismisses a toast', () => {
    const { result } = renderHook(() => useToast());
    let toastId: string;
    act(() => {
      const newToast = toast({ title: 'Test Toast' });
      toastId = newToast.id;
    });
    act(() => {
      result.current.dismiss(toastId);
    });
    expect(result.current.toasts[0].open).toBe(false);
  });

  it('removes a toast after delay', async () => {
    jest.useFakeTimers();
    const { result } = renderHook(() => useToast());
    let toastId: string;
    act(() => {
      const newToast = toast({ title: 'Test Toast' });
      toastId = newToast.id;
    });
    act(() => {
      result.current.dismiss(toastId);
      jest.advanceTimersByTime(1000000); // TOAST_REMOVE_DELAY
    });
    expect(result.current.toasts).toHaveLength(0);
    jest.useRealTimers();
  });

  it('dismisses all toasts when no toastId is provided', () => {
    const { result } = renderHook(() => useToast());
    act(() => {
      toast({ title: 'Toast 1' });
      toast({ title: 'Toast 2' });
    });
    act(() => {
      result.current.dismiss();
    });
    expect(result.current.toasts.every((t) => !t.open)).toBe(true);
  });
});