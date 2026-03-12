from typing import List, Any

def binary_search(arr: List[Any], target: Any) -> int:
    """
    Perform a binary search on a sorted array.

    Args:
        arr (List[Any]): A sorted list of elements.
        target (Any): The element to search for.

    Returns:
        int: The index of the target element if found, otherwise -1.
    """
    left, right = 0, len(arr) - 1  # Initialize left and right pointers

    while left <= right:
        mid = left + (right - left) // 2  # Calculate mid index to avoid potential overflow

        # Check if target is present at mid
        if arr[mid] == target:
            return mid  # Target found, return its index
        # If target is greater, ignore left half
        elif arr[mid] < target:
            left = mid + 1  # Move left pointer to mid + 1
        # If target is smaller, ignore right half
        else:
            right = mid - 1  # Move right pointer to mid - 1

    # Target was not found in the array
    return -1