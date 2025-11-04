import { render, screen } from '@testing-library/react';
import App from '../App';

test('renders main InsightBot UI', () => {
  render(<App />);

  // Headline
  expect(screen.getByText(/InsightBot/i)).toBeInTheDocument();

  // File input
  expect(screen.getByLabelText(/CSV File/i)).toBeInTheDocument();

  // Target column input
  expect(screen.getAllByPlaceholderText(/final_score/i).length).toBeGreaterThan(0);

  // Question input
  expect(
    screen.getByPlaceholderText(/Does hours studied impact final_score/i)
  ).toBeInTheDocument();

  // Submit button
  expect(screen.getByRole('button', { name: /submit/i })).toBeInTheDocument();
});
