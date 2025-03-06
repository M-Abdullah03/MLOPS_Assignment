import matplotlib.pyplot as plt
import numpy as np


def create_visualization(X_test, y_test, model):
    """Create a 3D visualization of the model predictions"""
    # Create a 3D plot
    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection='3d')

    # Scatter plot of the actual values
    ax.scatter(X_test['region_id'], X_test['time_slot'], y_test, color='blue', alpha=0.6, edgecolors='w')

    # Create a meshgrid for the plane
    x1 = np.linspace(X_test['region_id'].min(), X_test['region_id'].max(), num=10)
    x2 = np.linspace(X_test['time_slot'].min(), X_test['time_slot'].max(), num=10)
    x1, x2 = np.meshgrid(x1, x2)
    Z = model.coef_[0]*x1 + model.coef_[1]*x2 + model.intercept_

    # Plot the plane
    ax.plot_surface(x1, x2, Z, rstride=1, cstride=1, alpha=0.5, color='red')

    # Set labels
    ax.set_xlabel('Region ID', labelpad=10, fontsize=12, fontweight='bold')
    ax.set_ylabel('Time Slot', labelpad=10, fontsize=12, fontweight='bold')
    ax.set_zlabel('Gap', labelpad=10, fontsize=12, fontweight='bold')

    # Save plot
    plt.savefig('static/plot.png')
    plt.close()
