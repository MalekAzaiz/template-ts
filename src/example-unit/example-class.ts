export class MyClass {
  constructor(private readonly aNumber: number) {
  }

  get(): number {
    return this.aNumber;
  }
}
