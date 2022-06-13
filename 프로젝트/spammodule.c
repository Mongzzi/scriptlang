#include<Python.h>
#include<string.h>

static PyObject* spam_strlen(PyObject* self, PyObject* args) {
	char* str;
	int len;

	if (!PyArg_ParseTuple(args, "s", &str))
		return NULL;
	len = strlen(str);
	return Py_BuildValue("i", len);
}

static PyObject* spam_strlen_2(PyObject* self, PyObject* args) {
	char* str[4];
	int len[4];

	if (!PyArg_ParseTuple(args, "ssss", &str[0], &str[1], &str[2], &str[3]))
		return NULL;
	for (int i = 0;i < 4;++i)
		len[i] = strlen(str[i]);
	return Py_BuildValue("iiii", len[0], len[1], len[2], len[3]);
}

static PyObject* spam_itoa(PyObject* self, PyObject* args) {
	char* str[10] = {0,};
	int num;

	if (!PyArg_ParseTuple(args, "i", &num))
		return NULL;

	itoa(num, str, 10);
	return Py_BuildValue("s", str);
}

//3. 모듈에 등록할 함수 정의를 담은 배열 (__dict__ 속성이 됨)
static PyMethodDef SpamMethods[] = {
	{"strlen",spam_strlen, METH_VARARGS,"count a string length"},	//METH_VARARGS : 튜플
	{"strlen_2",spam_strlen_2, METH_VARARGS,"count a string length"},	//METH_VARARGS : 튜플
	{"itoa",spam_itoa, METH_VARARGS,"int to alpha"},
	{NULL,NULL,0,NULL}	// 배열 끝 표시
};

static PyModuleDef spammodule = {		// 2. 생성할 모듈 정보를 담는 구조체
	PyModuleDef_HEAD_INIT,
	"spam",
	"It is a test module.",
	-1,SpamMethods						// 3. SpamMethods 배열 참조
};


// 1. 파이썬 인터프리터에서 import할 때 실행
PyMODINIT_FUNC PyInit_spam(void) {
	return PyModule_Create(&spammodule);	// 2. spammoduel 구조체 잠조
}

// 빌드해서 생긴 ㅁㄴㅇㄹ.pyd를 C:\Python39\Lib 경로에 복사