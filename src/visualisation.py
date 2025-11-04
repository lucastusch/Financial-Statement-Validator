import matplotlib.pyplot as plt
import numpy as np


class BenfordVisualisation:
    """
    Benford's Law visualisation with a heatmap
    """

    def __init__(self, benford_results: dict, mad_value: float, interpretation: str):
        self.benford_results = benford_results
        self.mad_value = mad_value
        self.interpretation = interpretation

        # Convert all keys to integers and sort
        self.digits = sorted([int(d) for d in benford_results.keys()])
        self._prepare_data()

    def _prepare_data(self):
        """Extract data from Benford results"""
        expected_values = []
        actual_values = []

        for digit in self.digits:
            # Integer and string keys
            result = None
            if str(digit) in self.benford_results:
                result = self.benford_results[str(digit)]
            elif digit in self.benford_results:
                result = self.benford_results[digit]

            if result is not None:
                expected_values.append(result['expected_value'])
                actual_values.append(result['actual_value'])

        self.expected_values = np.array(expected_values)
        self.actual_values = np.array(actual_values)

    def display(self, figsize: tuple = (12, 6)):
        fig, ax = plt.subplots(figsize=figsize, dpi=100)

        # Prepare data for heatmap: rows are digits, columns are expected/actual
        data = np.array([self.expected_values, self.actual_values]).T

        # Create actual heatmap
        im = ax.imshow(data, cmap='RdYlGn', aspect='auto', vmin=0, alpha=0.8)

        # Labels
        ax.set_xticks([0, 1])
        ax.set_xticklabels(['Expected', 'Actual'], fontsize=12, fontweight='bold')
        ax.set_yticks(range(len(self.digits)))
        ax.set_yticklabels([f'Digit {d}' for d in self.digits], fontsize=11)

        ax.set_title('Benford\'s Law Analysis',
                     fontsize=14, fontweight='bold', pad=15)

        # Add value labels on heatmap
        for i in range(len(self.digits)):
            for j in range(2):
                value = data[i, j]
                ax.text(j, i, f'{value:.0f}', ha='center', va='center',
                        color='white' if value > np.max(data) / 2 else 'black',
                        fontsize=10, fontweight='bold')

        # Add colorbar
        cbar = plt.colorbar(im, ax=ax, orientation='vertical', pad=0.02)
        cbar.set_label('Count', fontsize=11, fontweight='bold')

        # Add MAD information as text
        mad_text = f'MAD Factor: {self.mad_value:.5f} | {self.interpretation}'
        fig.text(0.5, 0.02, mad_text, ha='center', fontsize=11,
                 style='italic', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.3))

        plt.tight_layout(rect=[0, 0.05, 1, 1])
        plt.show()

        return fig
