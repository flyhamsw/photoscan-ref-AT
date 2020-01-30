import PhotoScan
import os
import re
import time

class Innophotoscan:

    def __init__(self, epsg):
        print("InnoPAM")
        self.my_crs = PhotoScan.CoordinateSystem('EPSG::%s' % str(epsg))

    def photoscan_alignphotos(self, ImgList):
        start_time = time.time()

        # Prepare a document
        doc = PhotoScan.app.document
        chunk = doc.addChunk()
        chunk.addPhotos(ImgList)
        chunk.crs = self.my_crs

        # Retrieve georeferencing data of reference images
        doc.chunk.loadReference(
            'reference_query_merged.txt',
            PhotoScan.ReferenceFormatCSV,
            'n[XYZ]xyz',
            ','
        )

        # Start aerial triangulation
        print("==match Photos=================================================")
        print("===============================================================")
        chunk.matchPhotos(accuracy=PhotoScan.MediumAccuracy)

        print("==align photo==================================================")
        print("===============================================================")
        chunk.alignCameras()

        doc.save(path='result.psz', chunks=[doc.chunk])

        # Last image
        photo1 = chunk.cameras[-1]

        if not photo1.transform:
            print("There is no transformation matrix")

        XYZ = chunk.crs.project(chunk.transform.matrix.mulp(photo1.center))
        T = chunk.transform.matrix
        m = chunk.crs.localframe(T.mulp(photo1.center))  # transformation matrix to the LSE coordinates in the given point
        R = m * T * photo1.transform * PhotoScan.Matrix().Diag([1, -1, -1, 1])

        row = list()

        for j in range(0, 3):  # creating normalized rotation matrix 3x3
            row.append(R.row(j))
            row[j].size = 3
            row[j].normalize()

        R = PhotoScan.Matrix([row[0], row[1], row[2]])
        omega, phi, kappa = PhotoScan.utils.mat2opk(R)  # estimated orientation angles

        XYZ_list = list(XYZ)
        EO = [XYZ_list[0], XYZ_list[1], XYZ_list[2], kappa, phi, omega]

        print("===============================================================")
        print("===============================================================")
        print("===============================================================")
        print("==RESULT=======================================================")
        print("===============================================================")
        print("===============================================================")
        print("===============================================================")

        print('Query image name: %s' % photo1.label)
        print('Adjusted EO (X, Y, Z, kappa, phi, omega)')
        print(EO)

        print("process time = ", time.time() - start_time)

        return EO
