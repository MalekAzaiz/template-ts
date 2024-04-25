import math
import numpy as np 


class Operation : 
    """
    geometric operation that can be applied to a 2D vector (point) using a transformation matrix (mat)
    
    Args : 
        op_type  : operation type  [str]  ( options : translation,rotation,scaling)
        params  :  [all parameters must be numbers ]
            "translation"  -> [tx,ty]
            "rotation"     -> [angle_degree]
            "scaling"      -> [scale]   
    
    other attributes : 
        mat : operation matrix [matrix3x3]
        paramNames : name of each parameter [list] (tx,ty,angle_degree,scale)
        
               
    """
    def __init__(self, op_type:str, *args):
        self.type = op_type
        self.params = args
        
        self.generate_matrix()  
        print(self)
    
    def apply_on_Vector2D(self, vector):
        """apply the geometric operation on a Vector2D object 
        for homogenity , Vector2D -> [Vector2D.x,Vector2D.y,1]"""
        if self.mat is None:
            raise ValueError("Transformation matrix is not initialized.")
        
        if not isinstance(vector, Vector2D):
            raise ValueError("Input must be a Vector2D object.")
        
        # Convert the vector to homogeneous coordinates
        vector_homogeneous = np.array([vector.x, vector.y, 1])
        
        # apply the operation 
        result_vector = np.dot(self.mat.array, vector_homogeneous)
        
        # Convert back to Cartesian coordinates and return as a new Vector2D object
        return Vector2D(result_vector[0], result_vector[1])    
        
    def __repr__(self) -> str:
        params_repr = " // ".join([f"{name} = {value}" for name, value in zip(self.paramNames, self.params)])
        return f"\nOperation object:\n  type: {self.type}\n  params: {params_repr}\n  matrix: {self.mat}\n"

    def generate_matrix(self):
        """ generate the gemometric operation matrix """
        if self.type == "translation":
            self.mat = self.create_matrix_transation()
            
        elif self.type == "rotation":
            self.mat = self.create_matrix_rotation()
            
        elif self.type == "scaling":
            self.mat = self.create_matrix_scaling()
        else:
            raise ValueError("Unsupported operation type")
        
    def create_matrix_transation(self) :
        if len(self.params) != 2:
            raise ValueError("Translation requires two parameters: tx and ty")
        tx, ty = self.params
        self.paramNames = ['tx','ty']
        return Matrix3x3([1, 0, tx,0, 1, ty,0, 0, 1])
    def create_matrix_rotation(self) :
        if len(self.params) != 1:
            raise ValueError("Rotation requires one parameter: angle")
        angle_degree =self.params[0]
        self.paramNames = ['angle_degree']
        angle = angle_degree/180 * np.pi
        cos_theta = math.cos(angle)
        sin_theta = math.sin(angle)
        
        return Matrix3x3([
                cos_theta, -sin_theta, 0,
                sin_theta, cos_theta, 0 ,
                0, 0, 1 ] )
    def create_matrix_scaling(self) :
        if len(self.params) != 1:
            raise ValueError("Scaling requires one parameter: scale")
        scale = self.params[0]
        self.paramNames = ['scale']
        return Matrix3x3([scale, 0, 0, 0, scale, 0,0, 0, 1])

def test_operations():
    T = Operation("translation", 3, 4)
    vector_before = Vector2D(1, 1)
    result_after = T.apply_on_Vector2D(vector_before)
    assert result_after == Vector2D(4, 5)
    
    R = Operation("rotation", 90)
    vector_before = Vector2D(1,0)
    result_after = R.apply_on_Vector2D(vector_before)
    print(result_after)
    assert result_after == Vector2D(0,1)
    
    S = Operation("scaling", 2)
    vector_before = Vector2D(1, 1)
    result_after = S.apply_on_Vector2D(vector_before)
    assert result_after == Vector2D(2, 2)
    
    print("All operation tests passed successfully!")

class Vector2D:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
    
    def __repr__(self):
        return f"Vector2D : ({self.x=}, {self.y=})" 
    
    def __eq__(self, other):
        if not isinstance(other, Vector2D):
            return False
        return abs(self.x - other.x) < 1e-9 and abs(self.y - other.y) < 1e-9
    
class Matrix3x3:
    def __init__(self, elements:list):
        """
        elements : list containing row by row contents of the matrix 
        det : float for determinant 
        isInvertible : bool to descirbe the matrix's invertibility 
        
        """
        
        
        if len(elements) != 9:
            raise ValueError("Matrix must have 9 elements")
        self.array = np.array(elements).reshape((3, 3))
        self.det = np.linalg.det(self.array) # compute determinant
        self.isInvertible =  self.det != 0 
    
    def __repr__(self):
        rows = []
        for row in self.array:
            rows.append("    " + "   ".join(str(element) for element in row))
        return "Matrix 3x3:\n" + "\n".join(rows) 
    
    def __add__(self, other):
        if isinstance(other, Matrix3x3):
            result = self.array + other.array
            return Matrix3x3(result.ravel())
        elif isinstance(other, (int, float)):
            result = self.array + other
            return Matrix3x3(result.ravel())
        else:
            raise TypeError("Unsupported operand type(s) for +: 'Matrix3x3' and '{}'".format(type(other).__name__))
    
    def __sub__(self, other):
        if isinstance(other, Matrix3x3):
            result = self.array - other.array
            return Matrix3x3(result.ravel())
        elif isinstance(other, (int, float)):
            result = self.array - other
            return Matrix3x3(result.ravel())
        else:
            raise TypeError("Unsupported operand type(s) for -: 'Matrix3x3' and '{}'".format(type(other).__name__))

    def __mul__(self, other):
        if isinstance(other, Matrix3x3):
            return Matrix3x3(self.array.dot(other.array).flatten())
        elif isinstance(other, (int, float)) :
            return Matrix3x3(other*self.array.flatten())
        else : 
            raise TypeError("Unsupported operand type(s) for *: 'Matrix3x3' and '{}'".format(type(other).__name__))
        
    def inverse(self):
        """ if the matrix is invertible , returns the inverse as a matrix3x3 object 
        else it returns None """
        if self.isInvertible : 
            inverse_matrix = np.linalg.inv(self.array)
            return Matrix3x3(inverse_matrix.flatten())
        else : 
            print("Error: The matrix is not invertible.")
            return None
 
 
def test_Matrix3x3() : 
    # M1 = Matrix3x3([1, 2, 3, 2, 5, 6, 3, 6, 9])
    M1 = Matrix3x3([2, 1, -4, 3,3, -5, 4, 5, -2])
    M2 = Matrix3x3([1, 0, 0, 0, 1, 0, 0, 0, 1])
    # print(M1)
    # print(M2)

    # print(M1+M2)
    # print(M2+1)
    
    # print(M1-M2)
    # print(M2-1.2)
    
    # print(M1*M2)
    # print(M1*0)    
    # print(M1*1.1)
    
    # print(M1.inverse())    


if __name__ == "__main__":
    v1 = Vector2D(1, 2)
    v2 = Vector2D(3, 4)
    print(v1)

    # test_Matrix3x3()

    test_operations()
    # print(inv_M1.inverse)